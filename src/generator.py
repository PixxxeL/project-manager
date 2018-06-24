# -*- coding: utf-8 -*-

import commands
from distutils.dir_util import copy_tree
import json
import os
import re
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
        self.add_docs_info()
        self.add_readme()
        self.add_gitignore()
        self.commit('Init commit')
        self.route_type()
        self.commit('Base code')
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
        text = (u'# %s' % self.model['title'])
        for f in PROJECT_TYPES[self.model['type']]['readmes']:
            filepath = os.path.join(self.tmpl_dir, 'readmes', '%s.md' % f)
            text = u'%s\n\n%s' % (text, open(filepath, 'rb').read().decode('utf-8'),)
        open(path, 'wb').write(text.encode('utf-8'))

    def add_gitignore(self):
        src = os.path.join(self.tmpl_dir, 'common', '.gitignore')
        dst = os.path.join(self.repo_dir, '.gitignore')
        shutil.copy(src, dst)

    def add_docs_info(self):
        docs = os.path.join(self.pro_dir, 'docs')
        if not os.path.exists(docs):
            os.makedirs(docs)
        open(os.path.join(docs, 'info.txt'), 'wb')

    def add_batches(self, names=[]):
        if os.name != 'nt': # temporary!
            return # temporary!
        ext = 'bat' if os.name == 'nt' else 'sh'
        for name in names:
            src = os.path.join(
                self.tmpl_dir, 'batches', '%s.%s' % (name, ext,)
            )
            dst = os.path.join(
                self.pro_dir, '%s.%s' % (name, ext,)
            )
            shutil.copy(src, dst)

    def commit(self, message):
        os.chdir(self.repo_dir)
        self.call('git add .')
        self.call('git commit', ['-m "%s"' % message])
        os.chdir(self.pro_dir)

    def push(self):
        if not self.model['repo']:
            return
        os.chdir(self.repo_dir)
        self.call('git push origin master')
        os.chdir(self.pro_dir)

    def call(self, cmd, args=[]):
        if os.name == 'posix':
            print commands.getoutput('%s %s' % (cmd, ' '.join(args),))
        elif os.name == 'nt':
            cmds = cmd.split(' ')
            cmds.extend(args)
            subprocess.call(cmds, shell=True)
        else:
            print _(u'Ошибка команды %s' % cmd)

    def create_paths(self):
        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        self.tmpl_dir = os.path.join(self.app_dir, 'templates')
        self.pro_dir = os.path.join(self.model['path'], self.model['name'])
        self.repo_dir = os.path.join(self.pro_dir, 'repo')

    def route_type(self):
        print _(u'Копирование файлов проекта...')
        meth = getattr(self, PROJECT_TYPES[self.model['type']]['method'], None)
        if meth:
            meth()
        else:
            print _(u'\nОшибка!\nНет метода для этого типа...')

    def static_type(self, is_react=False, gulpfile=None):
        src = os.path.join(self.tmpl_dir, 'react' if is_react else 'static')
        dst = os.path.join(self.repo_dir, 'client')
        copy_tree(src, dst)
        if gulpfile:
            shutil.copy(
                os.path.join(self.tmpl_dir, gulpfile, 'gulpfile.js'),
                os.path.join(self.repo_dir, 'client', 'gulpfile.js')
            )
        os.chdir(dst)
        self.npm_init()
        self.bower_init()
        npm = REACT_NPM_PACKS if is_react else STATIC_NPM_PACKS
        if gulpfile == 'regular':
            npm = REGULAR_NPM_PACKS
        bower = REACT_BOWER_PACKS if is_react else STATIC_BOWER_PACKS
        self.call('npm i --save %s' % ' '.join(npm))
        self.call('bower i --save %s' % ' '.join(bower))
        self.call('gulp copy')
        self.call('gulp build') if is_react else self.call('gulp compile')
        os.chdir(self.pro_dir)
        batched = ['gulp', 'webpack'] if is_react else ['gulp']
        self.add_batches(batched)

    def static_with_php_type(self):
        self.static_type()
        dst = os.path.join(self.repo_dir, 'client')
        os.chdir(dst)
        self.call('git clone git@bitbucket.org:megatyumen-team/microfw.git scripts')
        scripts = os.path.join(dst, 'scripts')
        shutil.rmtree(os.path.join(scripts, '.git'), ignore_errors=True)
        os.remove(os.path.join(scripts, '.gitignore'))
        os.remove(os.path.join(scripts, 'README.md'))
        self.find_and_replace(
            os.path.join(dst, 'gulpfile.js'),
            re.compile(r'IS_PHP *= *false'),
            'IS_PHP = true'
        )
        os.rename(
            os.path.join(scripts, 'conf.template.php'),
            os.path.join(scripts, 'conf.php')
        )
        os.chdir(self.pro_dir)

    def pure_django_type(self):
        os.chdir(self.pro_dir)
        os.mkdir('media', self.dir_mode)
        src = os.path.join(self.tmpl_dir, 'django')
        dst = os.path.join(self.repo_dir, 'server')
        copy_tree(src, dst)
        self.call('virtualenv env')
        if os.name == 'posix':
            env = '../../env/bin/activate'
        elif os.name == 'nt':
            env = '..\\..\\env\\Scripts\\activate.bat'
        else:
            print _(u'Ошибка команды %s' % cmd)
        os.chdir(dst)
        self.call('%s & pip install -r requirements.txt' % env)
        os.chdir(self.pro_dir)
        self.add_batches(['envi', 'mana', 'runs'])
        self.static_type(
            is_react=(self.model['client_type'] == 1),
            gulpfile='regular'
        )

    def npm_init(self):
        data = {
            'name': self.model['name'],
            'version': '1.0.0',
            'description': '',
            'main': 'gulpfile.js',
            'scripts': {},
            'author': self.model['user'],
            'homepage': self.repo_site_url(),
            'repository': {
                'type': 'git',
                'url': self.repo_git_url(),
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
            'homepage': self.repo_site_url(),
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

    def repo_site_url(self):
        if self.model['repo'] == 1:
            return 'https://bitbucket.org/%(user)s/%(name)s' % self.model
        return ''

    def repo_git_url(self):
        if self.model['repo'] == 1:
            return 'git+ssh://git@bitbucket.org/%(user)s/%(name)s.git' % self.model
        return ''

    def find_and_replace(self, filepath, target_re, string):
        data = open(filepath, 'rb').read()
        data = target_re.sub(string, data)
        open(filepath, 'wb').write(data)

    def dev_generate(self):
        self.route_type()
