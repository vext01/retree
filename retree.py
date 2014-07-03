#!/usr/bin/env python3
import os, sys, re

class ReTreeError(Exception): pass

def do_rename(direc, filename, re_pairs):
    new_filename = filename
    for (re, repl) in re_pairs:
        new_filename = re.sub(repl, new_filename)

    if new_filename != filename:
        oldp, newp = (
                os.path.join(direc, filename),
                os.path.join(direc, new_filename))

        print("%s -> %s" % (oldp, newp))
        os.rename(oldp, newp)
    return new_filename

def recurse(path, re_pairs):
    renamed_files = [ do_rename(path, i, re_pairs) for i in os.listdir(path) ]

    for i in renamed_files:
        full_path = os.path.join(path, i)
        if os.path.isdir(full_path):
            recurse(full_path, re_pairs)

def usage():
        print("usage: retree <start_path> <pat_1> <repl_1> ... <pat_n> <repl_n>")
        sys.exit(1)

def entry_point():
    try:
        start_path = sys.argv[1]
    except IndexError:
        usage()

    regexs = sys.argv[2:]
    if not regexs or len(regexs) % 2 != 0:
        usage()

    re_pairs = [ (re.compile(regexs[i*2]), regexs[i*2+1]) for
            i in range(int(len(regexs) / 2)) ]

    os.chdir(start_path)
    recurse(".", re_pairs)

if __name__ == "__main__":
    entry_point()
