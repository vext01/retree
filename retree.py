#!/usr/bin/env python3
# Copyright (c) 2014, Edd Barrett <vext01@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION
# OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import os, sys, re

def do_rename(direc, filename, config):
    new_filename = filename

    if config.case == "l":
        new_filename = new_filename.lower()
    elif config.case == "u":
        new_filename = new_filename.upper()

    for (re, repl) in config.re_pairs:
        new_filename = re.sub(repl, new_filename)

    if new_filename != filename:
        oldp, newp = (
                os.path.join(direc, filename),
                os.path.join(direc, new_filename))

        print("%s -> %s" % (oldp, newp))
        os.rename(oldp, newp)
    return new_filename

def recurse(path, config):
    renamed_files = [ do_rename(path, i, config) for i in os.listdir(path) ]

    for i in renamed_files:
        full_path = os.path.join(path, i)
        if os.path.isdir(full_path):
            recurse(full_path, config)

def usage():
        print("usage: retree <start_path> <pat_1> <repl_1> ... <pat_n> <repl_n>")
        sys.exit(1)

class Config:
    def __init__(self):
        self.re_pairs = []
        self.case = None # 'l'/'u'/None

def entry_point():
    try:
        start_path = sys.argv[1]
    except IndexError:
        usage()

    rest = sys.argv[2:]
    config = Config()

    # Add argparse so we can change case and do regex on one invokation XXX
    if len(rest) == 1:
        if rest[0] in ["-l", "-u"]:
            config.case = rest[0][1]
        else:
            usage()
    else:
        if not rest or len(rest) % 2 != 0:
            usage()

        config.re_pairs = [ (re.compile(rest[i*2]), rest[i*2+1]) for
                i in range(int(len(rest) / 2)) ]

    if not os.path.isdir(start_path):
        do_rename(os.path.dirname(start_path),
                os.path.basename(start_path), re_pairs)
    else:
        os.chdir(start_path)
        recurse(".", config)

if __name__ == "__main__":
    entry_point()
