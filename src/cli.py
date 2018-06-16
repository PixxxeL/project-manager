# -*- coding: utf-8 -*-

#import os
import re
import sys

from choices import *
from generator import Generator


class Cli(object):

    def __init__(self):
        self.pro_re = re.compile(r'[^0-9a-z\-]+')
        self.model = _new_model()

    def run(self):
        self.get_project_path()
        self.get_project_name()
        self.get_project_title()
        self.get_project_type()
        self.get_project_repo()
        self.get_project_ide()
        Generator(self.model).generate()

    def get_project_path(self):
        ask = _(u'\nПуть до места, где будет папка проекта: ')
        inp = raw_input(ask)
        self.model['path'] = inp.strip() or '.'

    def get_project_name(self):
        ask = _(u'\nНазвание проекта (только латиница и дефис): ')
        inp = None
        while not inp:
            inp = raw_input(ask)
            inp = _(inp.strip()).lower()
            inp = self.pro_re.sub('', inp)
        self.model['name'] = inp

    def get_project_title(self):
        ask = _(u'\nНазвание проекта (на русском): ')
        inp = None
        while not inp:
            inp = raw_input(ask)
            inp = _(inp.strip())
        self.model['title'] = inp

    def get_project_type(self):
        self.model['type'] = self.ask_choices(
            u'\nТип проекта:',
            PROJECT_TYPES
        )

    def get_project_repo(self):
        self.model['repo'] = self.ask_choices(
            u'\nВнешний репозиторий:',
            PROJECT_REPOS
        )

    def get_project_ide(self):
        self.model['ide'] = self.ask_choices(
            u'\nРедактор кода:',
            PROJECT_IDES
        )

    def ask_choices(self, start_text, choices):
        print self.gen_choices(start_text, choices)
        inp = None
        keys = map(str, choices.keys())
        while not inp:
            inp = raw_input(_(u'Введите одну из цифр: '))
            if inp not in keys:
                inp = None
        return int(inp)

    def gen_choices(self, start_text, choices):
        text = u'%s\n' % start_text
        for k, v in choices.items():
            text = u'%s  %d) %s\n' % (text, k, v['title'],)
        return text


class StringEncoder(object):

    def __init__(self):
        self.coding = sys.stdout.encoding
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


def _new_model():
    return {
        'path' : '.',
        'name' : '',
        'title' : '',
        'type' : 0,
        'repo' : 0,
        'ide' : 0,
    }
