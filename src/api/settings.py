"""
Django settings for src project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import dj_database_url

ENABLE_API = not os.environ.get('ENABLE_API', 'y').lower() in ['n', 'no', 'false']
ENABLE_FRONT = os.environ.get('ENABLE_FRONT', 'n').lower() in ['y', 'yes', 'true']

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET', '1d5a5&y9(220)phk0o9cqjwdpm$3+**d&+kru(2y)!5h-_qn4b')
NB_WEBHOOK_KEY = os.environ.get('NB_WEBHOOK_KEY', 'prout')
NB_API_KEY = os.environ.get('NB_API_KEY', 'mustbesecret')
SENDGRID_SES_WEBHOOK_USER = os.environ.get('SENDGRID_SES_WEBHOOK_USER', 'fi')
SENDGRID_SES_WEBHOOK_PASSWORD = os.environ.get('SENDGRID_SES_WEBHOOK_PASSWORD', 'prout')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'true').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

# Application definition

INSTALLED_APPS = [
    # default contrib apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # security
    'corsheaders',

    # rest_framework
    'rest_framework',

    # geodjango
    'django.contrib.gis',
    'rest_framework_gis',

    # rules
    'rules.apps.AutodiscoverRulesConfig',

    # crispy forms
    'crispy_forms',

    # django filters
    'django_filters',

    #django_countries
    'django_countries',

    # fi apps
    'authentication',
    'people',
    'events',
    'groups',
    'clients',
    'lib',
    'front',
    'webhooks',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api.urls'

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

WSGI_APPLICATION = 'api.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default="postgis://api:password@localhost/api")
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.environ.get('STATIC_ROOT')

# Authentication

AUTH_USER_MODEL = 'authentication.Role'
AUTHENTICATION_BACKENDS = (
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
    'people.backend.PersonBackend',
)

# REST_FRAMEWORK

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'clients.authentication.AccessTokenAuthentication',
        'clients.authentication.ClientAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'lib.permissions.PermissionsOrReadOnly',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'EXCEPTION_HANDLER': 'api.handlers.exception_handler',
}

# Access tokens

AUTH_REDIS_URL = os.environ.get('AUTH_REDIS_URL', 'redis://localhost?db=0')
AUTH_REDIS_MAX_CONNECTIONS = 5
AUTH_REDIS_PREFIX = os.environ.get('AUTH_REDIS_PREFIX', 'AccessToken:')

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'WARNING')
LOG_FILE = os.environ.get('LOG_FILE', './errors.log')

if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'level': LOG_LEVEL,
                'class': 'logging.StreamHandler'
            },
            'file': {
                'level': LOG_LEVEL,
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOG_FILE,
                'backupCount': 3,
                'maxBytes': 5 * 1000 * 1000
            }
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True
            }
        }
    }

# SECURITY
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIAL = False
CORS_URLS_REGEX = r'^/legacy/'

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

if not DEBUG:
    # should be useless, but we never know
    # SECURE_SSL_REDIRECT = True
    # removed because it created problems with direct HTTP connections on localhost
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


if DEBUG:
    INSTALLED_APPS += ['silk']
    MIDDLEWARE.insert(0, 'silk.middleware.SilkyMiddleware')

CRISPY_TEMPLATE_PACK = 'bootstrap3'
