# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

import os

def db_config(database_name):
    """
    Creates a database configuration entry for Django.

    Arguments:
    - database_name (str): Name of the MySQL database that the configuration
      should apply to.
    """
    
    return {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.getenv('MYSQL_HOST'),
        'PORT': os.getenv('MYSQL_PORT', '3306'),
        'NAME': database_name,
        'USER': os.getenv('MYSQL_USER', 'django'),
        'PASSWORD': open(os.getenv('MYSQL_PASSWORD_FILE', '')).read().rstrip('\n')
    }



################################################################################
# DATABASES                                                                    #
################################################################################
# https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-DATABASES    #
#                                                                              #
# A dictionary containing the settings for all databases to be used with       #
# Django. It is a nested dictionary whose contents map a database alias to a   #
# dictionary containing the options for an individual database.                #
################################################################################

# IMPORTANT: When adding databases here, make sure to update the docker
# entry-point to build migrations for the new database by editing the DATABASES
# variable.

DATABASES = {
    'default': db_config(os.getenv('MYSQL_MAIN_DATABASE')),
    'graph': db_config(os.getenv('MYSQL_GRAPH_DATABASE'))
}



DATABASE_ROUTERS = ['api.dbrouters.ApiRouter']

################################################################################
# DEFAULT AUTO FIELD                                                           #
################################################################################
# Default primary key field type:                                              #
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field       #
################################################################################

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'