# -*- coding: utf-8 -*-

from distutils.dir_util import copy_tree
import json
import os
import subprocess
import shutil
import sys

import requests

from choices import *
from encoder import _


class Generator(object):

    dir_mode = 0755

    def __init__(self, model):
        self.call_dir = os.getcwd()
        self.model = model
        self.create_paths()

    def generate(self):
        self.make_project_dir()
        self.create_repo()
        self.create_ide_pro()
        self.add_readme()
        self.add_gitignore()
        self.commit('Init commit')
        self.route_type()
        self.push()

    def make_project_dir(self):
        print _(u'Создание директории проекта...')
        try:
            os.makedirs(self.pro_dir, self.dir_mode)
        except WindowsError:
            print _(u'\nОшибка!\nДиректория %s уже существует...' % self.pro_dir)
            sys.exit(1)
        os.chdir(self.pro_dir)

    def create_repo(self):
        print _(u'Создание локального репозитория...')
        os.mkdir(self.repo_dir, self.dir_mode)
        os.chdir(self.repo_dir)
        self.call('git init')
        self.create_remote_repo()
        os.chdir(self.pro_dir)

    def create_remote_repo(self):
        if not self.model['repo']:
            return
        print _(u'Создание удаленного репозитория...')
        if self.model['repo'] == 1:
            self.create_bitbucket_repo()
            remote_url = 'git@bitbucket.org:%(user)s/%(name)s.git' % self.model
        self.call('git remote add origin %s' % remote_url)

    def create_bitbucket_repo(self):
        url = 'https://api.bitbucket.org/2.0/repositories/%(user)s/%(name)s' % self.model
        lang = PROJECT_TYPES[self.model['type']]['language']
        data = {
            'scm': 'git',
            'is_private': 'true',
            'fork_policy': 'no_public_forks',
            'has_wiki': 'false',
            'has_issues': 'false',
            'language': lang,
            #'website': '',
            #'description': '',
        }
        conf = {
            'timeout' : 15,
            'headers' : {
                'User-Agent': 'New Project Generator',
                'Content-Type': 'application/json',
            },
            'auth' : (self.model['user'], self.model['password'],)
        }
        error = _(u'\nОшибка!\nНевозможно создать удаленный репозиторий...')
        try:
            response = requests.post(url, data=json.dumps(data), **conf)
        except:
            print error
            return
        if response.json().get('type') == 'error':
            print error
            print response.content

    def create_ide_pro(self):
        if not self.model['ide']:
            return
        print _(u'Создание проекта в IDE...')
        if self.model['ide'] == 1:
            src = os.path.join(
                self.tmpl_dir, 'common', 'project-name.sublime-project'
            )
            dst = os.path.join(
                self.pro_dir, '%s.sublime-project' % self.model['name']
            )
            shutil.copy(src, dst)

    def add_readme(self):
        path = os.path.join(self.repo_dir, 'readme.md')
        open(path, 'wb').write((u'# %s' % self.model['title']).encode('utf-8'))

    def add_gitignore(self):
        src = os.path.join(self.tmpl_dir, 'common', '.gitignore')
        dst = os.path.join(self.repo_dir, '.gitignore')
        shutil.copy(src, dst)

    def commit(self, message):
        os.chdir(self.repo_dir)
        self.call('git add .')
        self.call('git commit', ['-m "%s"' % message])
        os.chdir(self.pro_dir)

    def push(self):
        os.chdir(self.repo_dir)
        self.call('git push origin master')
        os.chdir(self.pro_dir)

    def call(self, cmd, args=[]):
        cmds = cmd.split(' ')
        cmds.extend(args)
        subprocess.call(cmds, shell=True)

    def create_paths(self):
        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        self.tmpl_dir = os.path.join(self.app_dir, 'templates')
        self.pro_dir = os.path.join(self.model['path'], self.model['name'])
        self.repo_dir = os.path.join(self.pro_dir, 'repo')

    def dev_generate(self):
        self.route_type()

    def route_type(self):
        print _(u'Копирование файлов проекта...')
        meth = getattr(self, PROJECT_TYPES[self.model['type']]['method'], None)
        if meth:
            meth()
        else:
            print _(u'\nОшибка!\nНет метода для этого типа...')

    def static_type(self):
        src = os.path.join(self.tmpl_dir, 'static')
        dst = os.path.join(self.repo_dir, 'client')
        copy_tree(src, dst)
        os.chdir(dst)
        self.npm_init()
        self.bower_init()
        self.call('npm i --save %s' % ' '.join(STATIC_NPM_PACKS))
        self.call('bower i --save %s' % ' '.join(STATIC_BOWER_PACKS))
        self.call('gulp copy')
        self.call('gulp compile')
        os.chdir(self.pro_dir)

    def npm_init(self):
        data = {
            'name': self.model['name'],
            'version': '1.0.0',
            'description': '',
            'main': 'gulpfile.js',
            'scripts': {},
            'author': self.model['user'],
            'homepage': 'https://bitbucket.org/%(user)s/%(name)s' % self.model,
            'repository': {
                'type': 'git',
                'url': 'git+ssh://git@bitbucket.org/%(user)s/%(name)s.git' % self.model,
            },
            'license': 'ISC',
            'dependencies': {}
        }
        json.dump(
            data,
            open(os.path.join(self.repo_dir, 'client', 'package.json'), 'wb')
        )

    def bower_init(self):
        data = {
            'name': self.model['name'],
            'description': '',
            'main': 'gulpfile.js',
            'authors': [
                self.model['user']
            ],
            'license': 'ISC',
            'homepage': 'https://bitbucket.org/%(user)s/%(name)s' % self.model,
            'private': True,
            'ignore': [
                '**/.*',
                'node_modules',
                'bower_components',
                'test',
                'tests'
            ],
            'dependencies': {}
        }
        json.dump(
            data,
            open(os.path.join(self.repo_dir, 'client', 'bower.json'), 'wb')
        )
