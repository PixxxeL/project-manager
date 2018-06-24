# -*- coding: utf-8 -*-

import sys


class StringEncoder(object):

    def __init__(self):
        self.coding = sys.stdout.encoding or 'utf-8'
        #if os.name == 'posix':
        #    self.coding = 'utf-8'
        #else:
        #    self.coding = 'cp866'

    def encode(self, string):
        return string.encode(self.coding)

    def decode(self, string):
        return string.decode(self.coding)


_encoder = StringEncoder()


def _(string):
    if isinstance(string, unicode):
        return _encoder.encode(string)
    else:
        return _encoder.decode(string)
