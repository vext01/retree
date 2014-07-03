#!/usr/bin/env python3
import os, sys

class ReTreeError(Exception): pass

def do_rename(path):
    # XXX just lowercases for now
    new_name = path.lower()

    print("%s -> %s" % (path, new_name))
    os.rename(path, new_name)

def recurse(path):
    for i in os.listdir(path):
        do_rename(os.path.join(path, i))

    # reread, since the filenames could have changed
    for i in os.listdir(path):
        full_path = os.path.join(path, i)
        if os.path.isdir(full_path):
            recurse(full_path)

def entry_point():
    # XXX read regex from commandline

    try:
        start_path = os.path.abspath(sys.argv[1])
    except IndexError:
        print("usage: retree <start_path>")
        sys.exit(1)

    recurse(start_path)

if __name__ == "__main__":
    entry_point()
