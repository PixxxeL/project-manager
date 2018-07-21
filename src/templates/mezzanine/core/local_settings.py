DEBUG = True

SECRET_KEY = '%SECRET_KEY%'
NEVERCACHE_KEY = '%NEVERCACHE_KEY%'

_ROOT_PATH = '%ROOT_PATH%'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '%s\\%PROJECT_NAME%.db' % _ROOT_PATH,
    }
}

ALLOWED_HOSTS = ['*']

STATIC_ROOT = '%s\\static' % _ROOT_PATH
MEDIA_ROOT = '%s\\media' % _ROOT_PATH

STATICFILES_DIRS = ('%s\\repo\\client' % _ROOT_PATH,)

INTERNAL_IPS = ['127.0.0.1']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST          = 'smtp.yandex.ru'
EMAIL_PORT          = 465
EMAIL_HOST_USER     = 'noreply@42dev.ru'
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_SSL       = True
DEFAULT_FROM_EMAIL  = 'noreply@42dev.ru'
SERVER_EMAIL        = 'noreply@42dev.ru'

PRODUCTION = (
    '8.8.8.8', 'webmaster', '',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(message)s'
        },
    },
    'handlers': {
        'trace': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '%s\\django.log' % _ROOT_PATH,
        }
    },
    'loggers': {
        'core': {
            'handlers': ['trace', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
