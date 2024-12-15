# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

import os;

################################################################################
# SECRET KEY                                                                   #
################################################################################

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-cq*agn1g35^_se)sirf%_bmztzme%)dxtkp=s*ll0l%=)!%sfk'



################################################################################
# ALLOWED HOSTS                                                                #
################################################################################

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '[::1]',
    '10.0.0.20'
]



################################################################################
# SECURE PROXY SSL HEADER                                                      #
################################################################################

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')



################################################################################
# CSRF TRUSTED ORIGINS                                                         #
################################################################################
# Trusted CSRF origins are fully-qualified domain names (including the scheme) #
# that you trust to safely send the CSRF token to.                             #
################################################################################

CSRF_TRUSTED_ORIGINS = [ 'https://csv.alexthomson.dev' ]