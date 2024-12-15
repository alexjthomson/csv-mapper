# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

import os;

################################################################################
# SECRET KEY                                                                   #
################################################################################
# SECURITY WARNING: Keep the secret key used in production secret!             #
################################################################################

def get_secret_key():
    """
    Reads the `SECRET_KEY` from a file specified by the `DJANGO_SECRET_KEY_FILE`
    environment variable.

    Returns:
    - str: The secret key if the file exists and is readable.
    
    Raises:
    - RuntimeError: If the file is not found or cannot be read.
    """
    
    secret_key_file = os.getenv('DJANGO_SECRET_KEY_FILE', '')
    if not secret_key_file:
        raise RuntimeError("Environment variable `DJANGO_SECRET_KEY_FILE` is not set.")

    try:
        with open(secret_key_file, 'r') as file:
            return file.read().rstrip('\n')
    except FileNotFoundError:
        raise RuntimeError(f"Secret key file '{secret_key_file}' not found.")
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading the secret key file: {e}")

# Gracefully set the `SECRET_KEY` or exit with a meaningful error:
try:
    SECRET_KEY = get_secret_key()
except RuntimeError as error:
    print(error)
    raise



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