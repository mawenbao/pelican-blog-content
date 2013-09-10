#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

import sys, md5

def slugify(inputStr):
    md5obj = md5.new()
    md5obj.update(inputStr)
    return "{} => #{}".format(inputStr, md5obj.digest().encode("hex"))

if __name__ == "__main__":
    print(slugify(sys.stdin.read().strip()))

