import os

from fabric.api import local, env, run, cd, prefix, local, lcd
from fabric.colors import green #, blue, cyan, magenta, red, white, yellow
from fabric.contrib.console import confirm
from core.local_settings import *


env.hosts    = [PRODUCTION[0]]
env.user     = PRODUCTION[1]
env.password = PRODUCTION[2]


def build():

    client_path = STATICFILES_DIRS[0]

    with lcd(client_path.replace('\\', '/')):

        is_build_static = False

        if confirm(green('Build styles?')):
            is_build_static = True
            local('gulp build')

        if confirm(green('Commit and push to repository?')):
            ci_desc = 'Static build' if is_build_static else 'Auto commit'
            with lcd('..'):
                local('git add . && git commit -m "%s"' % ci_desc)
                local('git push origin master')


def deploy():

    touch_path = '/home/webmaster/www'
    repo_path = '/home/webmaster/www/repo'

    with cd(repo_path):
        run('git pull origin master')

    with cd(repo_path), prefix('. ../env/bin/activate'):

        if confirm(green('Collectstatic?')):
            run('python server/manage.py collectstatic --noinput')

        if confirm(green('Migrate?')):
            run('python server/manage.py migrate')

    if confirm(green('Reload app?')):
        with cd(touch_path):
            run('touch touch-reload')


def build_and_deploy():
    build()
    deploy()
