#!/bin/bash
# @author: wilbur.ma@foxmail.com
# @date: 2013-09-09
# @license: BSD 3-Clause License
# @brief: set markdown h1 heading to title metadata
# @usage:
#   find content -name "*.md" -exec sh -c "./set_h1_to_title.sh {} > {}.new" \;
#   find content -name "*.md" -exec rename -f "s/\.new$//" {} \;

tac $1 | sed -r '/^#[^#]+/{h;d};/^Title: .*/{x}' | tac | sed -r '/^#[^#]+/{ s/^#/Title:/}'
