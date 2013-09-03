#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
# @author: wilbur.ma@foxmail.com
# @date: 2013-08-28
# @license: BSD 3-Clause License
# @brief: remove empty lines between lists
#         in a markdown file

import re, os, sys, optparse

UListLineRegex = re.compile("[+\-*][ \t]+.+")
OListLineRegex = re.compile("[1-9]+[.][ \t]+.+")

def is_list_line(line):
    return UListLineRegex.match(line) or OListLineRegex.match(line)

def is_empty_list_line(lines, lineInd):
    if (lineInd < 0) or (lineInd >= len(lines)):
        return True
    if (0 == lineInd) or (len(lines) == lineInd + 1):
        return False
    if lines[lineInd].rstrip("\n"):
        return False
    # find the first non-empty previous line
    firstNEmptyLineInd = lineInd - 1
    lastNEmptyLineInd = lineInd + 1
    prevListLineFound = False
    postListLineFound = False
    while firstNEmptyLineInd >= 0:
        if not lines[firstNEmptyLineInd].rstrip("\n"):
            firstNEmptyLineInd -= 1
        else:
            prevListLineFound = is_list_line(lines[firstNEmptyLineInd])
            break
    if not prevListLineFound:
        return False
    while lastNEmptyLineInd < len(lines):
        if not lines[lastNEmptyLineInd].rstrip("\n"):
            lastNEmptyLineInd += 1
        else:
            postListLineFound = is_list_line(lines[lastNEmptyLineInd])
            break
    return prevListLineFound and postListLineFound

def remove_empty_list_lines(fileobj):
    lines = fileobj.readlines()
    if not lines:
        return []
    return [lines[ind]
                for ind in xrange(len(lines))
                    if not is_empty_list_line(lines, ind)]

if __name__ == "__main__":
    cmdParser = optparse.OptionParser()
    cmdParser.add_option("-i", "--in-place", dest="inPlace", action="store_true", help="Overwrite file directly")
    options, args = cmdParser.parse_args()

    if not args:
        print("ERROR: no input file")
        sys.exit(1)

    for filePath in args:
        if not os.path.isfile(filePath):
            print("ERROR: {} is not a regular file".format(filePath))
            sys.exit(2)

        lines = None
        with open(filePath, "r") as f:
            lines = "".join(remove_empty_list_lines(f))
        if options.inPlace:
            with open(filePath, "w") as f:
                f.write(lines)
        else:
            sys.stdout.write(lines)

