# -*- coding: utf-8 -*-

import getpass
import re

from choices import *
from generator import Generator
from encoder import _


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
        if self.model['type'] in [4]:
            self.model['client_type'] = self.ask_choices(
                u'\nТип клиентской части проекта:',
                PROJECT_CLIENT_TYPES
            )

    def get_project_repo(self):
        self.model['repo'] = self.ask_choices(
            u'\nУдаленный репозиторий:',
            PROJECT_REPOS
        )
        self.get_repo_user()
        self.get_repo_password()

    def get_repo_user(self):
        if not self.model['repo']:
            return
        ask = _(u'\nЛогин на удаленном репозитории: ')
        inp = None
        while not inp:
            inp = raw_input(ask)
            inp = _(inp.strip())
        self.model['user'] = inp

    def get_repo_password(self):
        if not self.model['repo']:
            return
        ask = _(u'\nПароль на удаленном репозитории: ')
        inp = None
        while not inp:
            print ask,
            inp = getpass.getpass('')
            #inp = getpass.getpass(ask)
            inp = _(inp.strip())
        self.model['password'] = inp

    def get_project_ide(self):
        self.model['ide'] = self.ask_choices(
            u'\nРедактор кода:',
            PROJECT_IDES
        )

    def ask_choices(self, start_text, choices):
        print _(self.gen_choices(start_text, choices))
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

    def dev_run(self):
        #self.get_project_type()
        self.get_repo_password()
        Generator(self.model).dev_generate()


def _new_model():
    return {
        'path' : 'C:\\Users\\pix\\dev\\pro',
        'name' : 'test-django-project',
        'title' : u'Тестовый проект',
        'type' : 4,
        'repo' : 0,
        'ide' : 0,
        'user' : 'pixxxel',
        'password' : '',
        'client_type' : 0,
    }
