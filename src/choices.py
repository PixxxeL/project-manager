# -*- coding: utf-8 -*-

PROJECT_TYPES = {
    1 : {
        'title' : u'Статический (Jade, CoffeeScript, SASS)',
        'language' : 'html/css',
        'method' : 'static_type',
        'readmes' : ['static-client'],
    },
    2 : {
        'title' : u'Статический с PHP',
        'language' : 'html/css',
        'method' : 'static_with_php_type',
        'readmes' : ['static-php-client', 'static-client'],
    },
    #3 : {
    #    'title' : u'Сайт на Joomla',
    #    'language' : 'php',
    #    'method' : '',
    #    'readmes' : [''],
    #},
    4 : {
        'title' : u'Чистый Django 1.11',
        'language' : 'python',
        'method' : 'pure_django_type',
        'readmes' : ['pure-django'],
    },
    #5 : {
    #    'title' : u'Grappelli',
    #    'language' : 'python',
    #    'method' : '',
    #    'readmes' : [''],
    #},
    6 : {
        'title' : u'Mezzanine',
        'language' : 'python',
        'method' : 'mezzanine_type',
        'readmes' : ['pure-django'],
    },
}

PROJECT_CLIENT_TYPES = {
    0 : {
        'title' : u'Без клиента',
    },
    1 : {
        'title' : u'Стандартный',
    },
    2 : {
        'title' : u'React',
    },
}

PROJECT_REPOS = {
    0 : {
        'title' : u'Без создания репозитория',
    },
    1 : {
        'title' : u'Приватный репозиторий на Bitbucket',
    },
    2 : {
        'title' : u'Публичный репозиторий на Github',
    },
    3 : {
        'title' : u'Приватный репозиторий на GitLab.42dev.ru',
    },
}

PROJECT_IDES = {
    0 : {
        'title' : u'Без создания проекта в IDE',
    },
    1 : {
        'title' : u'Проект в Sublime Text 3',
    },
}

GITLAB_NAMESPACES = {
    6 : {
        'title' : 'livefeed',
    },
    7 : {
        'title' : 'tools',
    },
    8 : {
        'title' : 'gpn',
    },
    9 : {
        'title' : 'sites',
    },
    10 : {
        'title' : 'portals',
    },
    11 : {
        'title' : 'services',
    },
    12 : {
        'title' : 'misc',
    },
    14 : {
        'title' : 'packages',
    },
}

STATIC_NPM_PACKS = [
    'gulp', 'gutil', 'del', 'gulp-sass', 'gulp-jade', 'gulp-coffee@2.3.5',
    'gulp-shell', 'gulp-rename', 'gulp-sourcemaps', 'gulp-yuicompressor',
    'gulp-concat', 'gulp-zip', 'gulp-html-replace'
]

STATIC_BOWER_PACKS = [
    'jquery-legacy=jquery#1.12.4', 'jquery-modern=jquery#2.2.4',
    'font-awesome#4.7.0', 'html5-boilerplate', 'html5shiv', 'respond'
]

REACT_NPM_PACKS = [
    'gulp', 'gulp-sass', 'gulp-shell', 'gulp-sourcemaps', 'gutil',
    'babel-core', 'babel-loader', 'babel-polyfill', 'babel-preset-es2015',
    'babel-preset-react', 'css-loader', 'json-loader', 'react', 'react-dom', 
    'style-loader', 'webpack@3.8.1', 'axios', 'universal-cookie', 'react-popup',
    'moment'
]

ADDIT_REACT_PACKS = [ # not used yet
    'react-select', 'react-flatpickr', 'react-avatar-editor', 'react-paginate'
]

REACT_BOWER_PACKS = [
    'font-awesome#4.7.0', 'html5-boilerplate', 'html5shiv', 'respond'
]

REGULAR_NPM_PACKS = [
    'gulp', 'gutil', 'gulp-sass', 'gulp-coffee@2.3.5', 'gulp-rename',
    'gulp-sourcemaps', 'gulp-yuicompressor', 'gulp-concat-sourcemap',
    'gulp-shell'
]
