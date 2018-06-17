# -*- coding: utf-8 -*-

PROJECT_TYPES = {
    1 : {
        'title' : u'Статический полностью',
        'language' : 'html/css',
        'method' : 'static_type',
    },
    #2 : {
    #    'title' : u'Статический с PHP',
    #    'language' : 'html/css',
    #},
    #3 : {
    #    'title' : u'Сайт на Joomla',
    #    'language' : 'php',
    #},
    #4 : {
    #    'title' : u'На Django 1.11',
    #    'language' : 'python',
    #},
    #5 : {
    #    'title' : u'На Django 1.11 и React',
    #    'language' : 'python',
    #},
    #6 : {
    #    'title' : u'На Mezzanine',
    #    'language' : 'python',
    #},
}

PROJECT_REPOS = {
    0 : {
        'title' : u'Без создания репозитория',
    },
    1 : {
        'title' : u'Репозиторий на Bitbucket',
    },
    #2 : {
    #    'title' : u'Репозиторий на Github',
    #},
}

PROJECT_IDES = {
    0 : {
        'title' : u'Без создания проекта в IDE',
    },
    1 : {
        'title' : u'Проект в Sublime Text 3',
    },
}

STATIC_NPM_PACKS = [
    'gulp', 'gutil', 'del', 'gulp-sass', 'gulp-jade', 'gulp-coffee',
    'gulp-shell', 'gulp-rename', 'gulp-sourcemaps', 'gulp-yuicompressor',
    'gulp-concat', 'gulp-zip', 'gulp-html-replace'
]

STATIC_BOWER_PACKS = [
    'jquery-legacy=jquery#1.12.4', 'jquery-modern=jquery#2.2.4',
    'font-awesome#4.7.0', 'html5-boilerplate', 'html5shiv', 'respond'
]
