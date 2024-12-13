################################################################################
# INSTALLED APPS                                                               #
################################################################################
# https://docs.djangoproject.com/en/5.0/ref/applications/                      #
#                                                                              #
# This is a list of strings designating all of the applications that are       #
# enabled in this Django instance. An app is a web application that does       #
# something - e.g., a blog, a database or public records, or a small poll app. #
################################################################################

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'account',
    'api',
    'dashboard'
]



################################################################################
# MIDDLEWARE                                                                   #
################################################################################
# https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-MIDDLEWARE   #
#                                                                              #
# This is a list of middleware classes that process requests and responses.    #
# Middleware is a framework of hooks into Django's request/response            #
# processing. It is a lightweight, low-level plugin system for globally        #
# altering Django's input or output. Each middleware component is responsible  #
# for doing some specific function. For example, Django includes middleware to #
# handle sessions, CSRF protection, authentication, and more.                  #
################################################################################

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



################################################################################
# ROOT URL CONFIGURATION                                                       #
################################################################################
# This denotes the Python module where your URL patterns live. This is the     #
# module that contains the `urlpatterns` variable. Django uses this variable   #
# to match incoming HTTP requests against the available URLs to find the       #
# correct view.                                                                #
################################################################################

ROOT_URLCONF = 'csv_mapper.urls'



################################################################################
# TEMPLATES                                                                    #
################################################################################
# This is a configuration dictionary containing settings for the template      #
# engine, which is the part of Django that merges data with templates to       #
# produce the final HTML output. This setting specifies backend details,       #
# directories to search for templates, context processors, and more.           #
################################################################################

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]



################################################################################
# WSGI APPLICATION                                                             #
################################################################################
# This is a string pointing to the WSGI application callable, which is used by #
# WSGI servers to communicate with the Django application. It acts as the      #
# entry-point for WSGI-compatible web-servers to serve your project.           #
################################################################################

WSGI_APPLICATION = 'csv_mapper.wsgi.application'