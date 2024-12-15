# PROJECT SETTINGS
# This directory contains the settings for the project. The settings have been
# split into different files to make them easier to find and manage. There are
# also deployment environment specific setting overrides depending on the value
# of the `DJANGO_ENVIRONMENT` environment variable.

# For more information on this file, see:
# https://docs.djangoproject.com/en/5.0/topics/settings/

# For the full list of settings and their values, see:
# https://docs.djangoproject.com/en/5.0/ref/settings/

import os



################################################################################
# BASE DIRECTORY                                                               #
################################################################################
# The base directory is used to get the base directory of the Django project.  #
# This is used by other settings scripts to reference other project files.     #
################################################################################

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent



################################################################################
# STATIC FILES                                                                 #
################################################################################
# https://docs.djangoproject.com/en/5.0/howto/static-files/                    #
#                                                                              # 
# In development environments (or any environment where `DEBUG` is `True`),    #
# static content is hosted by Django; however, in production environments (or  #
# any environment where `DEBUG` is `False`), Django does not.                  #
#                                                                              #
# In these cases, additional software such as nginx is required to host the    #
# static content for Django.                                                   #
################################################################################

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'static') ]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]



################################################################################
# DEBUG MODE                                                                   #
################################################################################
# SECURITY WARNING: Do not run with `DEBUG` as `True` in production            #
# environments. For security reasons, this will default to `False` and should  #
# be overwritten depending on the deployment environment.                      #
################################################################################

DEBUG = False



################################################################################
# SETTINGS IMPORTS                                                             #
################################################################################
# Different parts of the application have been split into different settings   #
# files. This allows settings to be organised; making them easier to find and  #
# modify.                                                                      #
################################################################################

from .apps import *
from .databases import *
from .internationalisation import *
from .logging import *
from .login import *
from .passwords import *
from .security import *

# Get the deployment environment specific setting overrides:
environment = os.getenv('DJANGO_ENVIRONMENT', 'DEVELOPMENT')
if environment == 'DEVELOPMENT':
    from .environments.development import *
elif environment == 'PRODUCTION':
    from .environments.production import *
else:
    import logging
    logger = logging.getLogger(__name__)
    logger.error(f'Unknown deployment environment `{environment}`. Please choose from `DEVELOPMENT` or `PRODUCTION`.')
    import sys
    sys.exit(1)