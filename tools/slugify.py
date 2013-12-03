#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
# @author: wilbur.ma@foxmail.com
# @date: 2013-09-09
# @license: BSD 3-Clause License
# @brief: the default slugify function used by extract_headings plugin
# @usage: grep '^#' content/pages/about.md | sed 's/#//g' | xargs -d '\n' ./slugify.py

import sys, md5, optparse

def slugify(inputStr):
    md5obj = md5.new()
    md5obj.update(inputStr)
    return "#{} <= {}".format(md5obj.digest().encode("hex"), inputStr)

if __name__ == "__main__":
    parser = optparse.OptionParser()
    options, args = parser.parse_args()

    if len(args) > 0:
        for inputStr in args:
            print(slugify(inputStr.strip()))
    else:
        inputStr = sys.stdin.read()
        print(slugify(inputStr.strip()))

