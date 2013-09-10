# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals

from HTMLParser import HTMLParser
from pelican import signals, contents

class FirstParagraphParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.paragraphTag = 'p'
        self.data = ''
        self.currTags = []

    def handle_starttag(self, tag, attrs):
        if not self.data and self.paragraphTag == tag.lower():
            self.currTags.append('p')
        elif self.currTags:
            self.currTags.append(tag)

    def handle_endtag(self, tag):
        if self.currTags:
            self.currTags.pop()

    def handle_data(self, data):
        if self.currTags:
            self.data += data

def content_object_init(instance):
    if isinstance(instance, contents.Static):
        return
    if 'summary' in instance.metadata:
        return
    if not hasattr(instance, '_summary') and instance._content is not None:
        content = instance.content
        firstP = FirstParagraphParser()
        firstP.feed(content)
        endCharA = '。'
        endCharB = '.'
        endPosA = firstP.data.find(endCharA)
        endPosB = firstP.data.find(endCharB)
        endPos = endPosA if endPosA > endPosB else endPosB
        instance._summary = firstP.data[:endPos + 1 if endPos > 0 else -1]

def register():
    signals.content_object_init.connect(content_object_init)
