# -*- coding: utf-8 -*-

import json
import getpass
from optparse import OptionParser
import os
import re
import sys

from choices import *
from generator import Generator
from encoder import _


class Cli(object):

    commands = ['start', 'pull', 'deploy', 'publish', 'extend']
    config_fields = ['path', 'user', 'gitlab_token']

    def __init__(self):
        self.commandline_parse()
        self.pro_re = re.compile(r'[^0-9a-z\-]+')
        self.model = self.get_default_model()
        self.load_config()

    def run(self):
        getattr(self, self.command)()
        self.save_config()

    def start(self):
        self.get_project_path()
        self.get_project_name()
        self.get_project_title()
        self.get_project_type()
        self.get_project_repo()
        self.get_project_ide()
        Generator(self.model).generate()

    def pull(self):
        raise NotImplementedError('Method not ready yet!')

    def deploy(self):
        raise NotImplementedError('Method not ready yet!')

    def publish(self):
        raise NotImplementedError('Method not ready yet!')

    def extend(self):
        raise NotImplementedError('Method not ready yet!')

    def get_project_path(self):
        if self.model['path']:
            return
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
        ask = _(u'\nНазвание проекта (можно на русском): ')
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
        if self.model['type'] in [4, 5, 6]:
            self.model['client_type'] = self.ask_choices(
                u'\nТип клиентской части проекта:',
                PROJECT_CLIENT_TYPES
            )

    def get_project_repo(self):
        self.model['repo'] = self.ask_choices(
            u'\nУдаленный репозиторий:',
            PROJECT_REPOS
        )
        if self.model['repo'] in [1, 2]:
            self.get_repo_user()
            self.get_repo_password()
        elif self.model['repo'] == 3:
            self.get_gitlab_token()
            self.get_repo_namespace()

    def get_repo_user(self):
        if not self.model['repo'] or self.model['user']:
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

    def get_gitlab_token(self):
        if not self.model['repo'] or self.model['gitlab_token']:
            return
        ask = _(u'\nPrivate token для GitLab: ')
        inp = None
        while not inp:
            inp = raw_input(ask)
            inp = _(inp.strip())
        self.model['gitlab_token'] = inp

    def get_repo_namespace(self):
        if not self.model['repo']:
            return
        self.model['gitlab_group'] = self.ask_choices(
           u'\nГруппа проекта:',
           GITLAB_NAMESPACES
        )

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

    def commandline_parse(self):
        '''
        Должен вызываться первым
        '''
        parser = OptionParser(usage='%s [options]' % '|'.join(self.commands))
        parser.add_option(
            '-c', '--config-file', action="store", dest='config_file',
            default='config.json', help='Full path to config file'
        )
        (options, args) = parser.parse_args()
        self.command = args[0] if args and args[0] in self.commands else 'start'
        self.config_file = options.config_file

    def load_config(self):
        '''
        Должен вызываться после `self.model = self.get_default_model()`
        '''
        if getattr(sys, 'frozen', False):
            cur_dir = os.path.dirname(sys.executable)
        elif __file__:
            cur_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            cur_dir = os.getcwd()
        if self.config_file == 'config.json':
            self.config_file = os.path.join(cur_dir, self.config_file)
        try:
            config = json.load(open(self.config_file, 'rb')) or {}
            print _(u'Конфигурация загружена из файла: %s' % self.config_file)
        except:
            config = {}
        for field in self.config_fields:
            self.model[field] = config.get(field, self.model[field])

    def save_config(self):
        '''
        Предпочтительно вызывать в конце
        '''
        config = {}
        for field in self.config_fields:
            config[field] = self.model[field]
        json.dump(config, open(self.config_file, 'wb'))
        print _(u'Конфигурация записана в файл: %s' % self.config_file)

    def get_default_model(self):
        return {
            'path' : '',
            'name' : 'test-django-project',
            'title' : u'Тестовый проект',
            'type' : 4,
            'repo' : 0,
            'ide' : 0,
            'user' : '',
            'password' : '',
            'gitlab_group' : '',
            'gitlab_token' : '',
            'client_type' : 0,
        }
