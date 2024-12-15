import os

LOG_LEVEL = os.getenv('DJANGO_LOG_LEVEL', 'WARNING')
LOG_DIR = os.environ.get('DJANGO_LOG_DIRECTORY', '/log') # This can be used to override the log directory during unit testing

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '{name} {levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{'
        }
    },
    'handlers': {
        'application_file': {
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOG_DIR, 'application.log'),
            'level': LOG_LEVEL
        },
        'core_file': {
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOG_DIR, 'core.log'),
            'level': LOG_LEVEL
        },
        'django_file': {
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOG_DIR, 'django.log'),
            'level': LOG_LEVEL
        },
        'request_file': {
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOG_DIR, 'request.log'),
            'level': LOG_LEVEL
        },
        'db_file': {
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOG_DIR, 'db.log'),
            'level': LOG_LEVEL
        }
    },
    'loggers': {
        '': {
            'level': LOG_LEVEL,
            'handlers': [ 'application_file' ],
        },
        'root': {
            'level': LOG_LEVEL,
            'handlers': [ 'application_file' ],
        },
        'core': {
            'level': LOG_LEVEL,
            'handlers': [ 'core_file' ],
            'propagate': True,
        },
        'django': {
            'level': LOG_LEVEL,
            'handlers': [ 'django_file' ],
            'propagate': True,
        },
        'django.request': {
            'level': LOG_LEVEL,
            'handlers': [ 'request_file' ],
            'propagate': True,
        },
        'django.db.backends': {
            'level': LOG_LEVEL,
            'handlers': [ 'db_file' ],
            'propagate': True,
        }
    }
}