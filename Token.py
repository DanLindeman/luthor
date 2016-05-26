#!usr/bin/env python3

class Token(object):

    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

    def __str__(self):
        return "<{0.kind}: {0.value}>".format(self)
