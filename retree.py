#!/usr/bin/env python3
import os, sys, re

class ReTreeError(Exception): pass

def do_rename(path, re_pairs):
    # XXX just lowercases for now
    new_name = path
    for (re, repl) in re_pairs:
        new_name = re.sub(repl, new_name)

    if new_name != path:
        print("%s -> %s" % (path, new_name))
        os.rename(path, new_name)

def recurse(path, re_pairs):
    for i in os.listdir(path):
        do_rename(os.path.join(path, i), re_pairs)

    # reread, since the filenames could have changed
    for i in os.listdir(path):
        full_path = os.path.join(path, i)
        if os.path.isdir(full_path):
            recurse(full_path, re_pairs)

def usage():
        print("usage: retree <start_path> <pat_!> <repl_1> ... <pat_n> <repl_n>")
        sys.exit(1)

def entry_point():
    # XXX read regex from commandline

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
