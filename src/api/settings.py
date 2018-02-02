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
import dj_email_url
from django.contrib.messages import ERROR

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'true').lower() == 'true'

ENABLE_API = not os.environ.get('ENABLE_API', 'y').lower() in ['n', 'no', 'false']
ENABLE_FRONT = os.environ.get('ENABLE_FRONT', 'n').lower() in ['y', 'yes', 'true'] or DEBUG
ENABLE_MAP = os.environ.get('ENABLE_MAP', 'n').lower() in ['y', 'yes', 'true'] or DEBUG

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
MAILTRAIN_API_KEY = os.environ.get('MAILTRAIN_API_KEY', 'prout')

# these domain names are used when absolute URLs should be generated (e.g. to include in emails)
MAIN_DOMAIN = os.environ.get('MAIN_DOMAIN', 'https://lafranceinsoumise.fr')
API_DOMAIN = os.environ.get('API_DOMAIN', 'http://localhost:8000' if DEBUG else 'https://api.lafranceinsoumise.fr')
FRONT_DOMAIN = os.environ.get('FRONT_DOMAIN', 'http://localhost:8000' if DEBUG else 'https://agir.lafranceinsoumise.fr')
MAP_DOMAIN = os.environ.get('MAP_DOMAIN', 'http://localhost:8000' if DEBUG else 'https://agir.lafranceinsoumise.fr')
MAILTRAIN_HOST = os.environ.get('MAILTRAIN_HOST', 'http://localhost:8080')
MAILTRAIN_LIST_ID = os.environ.get('MAILTRAIN_LIST_ID', 'SyWda9pi')
MAILTRAIN_DISABLE = DEBUG

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

    # redirect
    'django.contrib.sites',
    'django.contrib.redirects',

    # security
    'corsheaders',

    # rest_framework
    'rest_framework',

    # OTP for admin
    'django_otp',
    'django_otp.plugins.otp_totp',

    # geodjango
    'django.contrib.gis',
    'rest_framework_gis',

    # rules
    'rules.apps.AutodiscoverRulesConfig',

    # crispy forms
    'crispy_forms',

    # django filters
    'django_filters',

    # django_countries
    'django_countries',

    # ajax_select
    'ajax_select',

    # phone number field
    'phonenumber_field',

    # admin steroids
    'admin_steroids',

    # stdimage
    'stdimage',

    # webpack
    'webpack_loader',

    # fi apps
    'authentication',
    'people',
    'events',
    'groups',
    'polls',
    'clients',
    'lib',
    'front',
    'carte',
    'webhooks',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware'
]

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ['127.0.0.1']


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
                'api.context_processors.domain_names'
            ],
        },
    },
]

MESSAGE_TAGS = {
    ERROR: 'danger'
}

WSGI_APPLICATION = 'api.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default="postgis://api:password@localhost/api")
}

# Mails

# by default configured for mailhog sending
email_config = dj_email_url.parse(os.environ.get('SMTP_URL', 'smtp://localhost:1025/'))

EMAIL_FILE_PATH = email_config['EMAIL_FILE_PATH']
EMAIL_HOST_USER = email_config['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = email_config['EMAIL_HOST_PASSWORD']
EMAIL_HOST = email_config['EMAIL_HOST']
EMAIL_PORT = email_config['EMAIL_PORT']
EMAIL_BACKEND = email_config['EMAIL_BACKEND']
EMAIL_USE_TLS = email_config['EMAIL_USE_TLS']
EMAIL_USE_SSL = email_config['EMAIL_USE_SSL']

# fixed for now ==> maybe more flexible?
EMAIL_TEMPLATES = {
    # WELCOME_MESSAGE variables: [PROFILE_LINK]
    "WELCOME_MESSAGE": "https://mosaico.jlm2017.fr/emails/ac205f71-61a3-465b-8161-cec5729ecdbb.html",
    # UNSUBSCRIBE_CONFIRMATION variables [MANAGE_SUBSCRIPTIONS_LINK]
    "UNSUBSCRIBE_CONFIRMATION": "https://mosaico.jlm2017.fr/emails/51cbadd7-2226-482d-85d4-6dc758d2eb3a.html",
    # GROUP_CREATION variables: [GROUP_NAME], [CONTACT_{NAME,EMAIL,PHONE,PHONE_VISIBILITY], [LOCATION_{NAME,LOCATION}], [GROUP_LINK], [MANAGE_GROUP_LINK]
    "GROUP_CREATION": "https://mosaico.jlm2017.fr/emails/bc07d593-ff8f-470e-a8cb-9ba679fc5f59.html",
    # GROUP_CHANGED variables: GROUP_NAME, GROUP_CHANGES, GROUP_LINK
    "GROUP_CHANGED": "https://mosaico.jlm2017.fr/emails/3724b7ba-2a48-4954-9496-fc4c970a56b8.html",
    # GROUP_SOMEONE_JOINED_NOTIFICATION variables: GROUP_NAME, PERSON_INFORMATION, MANAGE_GROUP_LINK
    'GROUP_SOMEONE_JOINED_NOTIFICATION': "https://mosaico.jlm2017.fr/emails/e25c5123-6a7d-428f-89c6-3ddca4a65096.html",
    # EVENT_CREATION variables: [EVENT_NAME], [CONTACT_{NAME,EMAIL,PHONE,PHONE_VISIBILITY], [LOCATION_{NAME,LOCATION}], [EVENT_LINK], [MANAGE_EVENT_LINK]
    'EVENT_CREATION': "https://mosaico.jlm2017.fr/emails/f44ff2c1-1050-41c4-8973-15573eba2741.html",
    # EVENT_CHANGED variables: EVENT_NAME, EVENT_CHANGES, EVENT_LINK, EVENT_QUIT_LINK
    "EVENT_CHANGED": "https://mosaico.jlm2017.fr/emails/f8dfc882-4e7e-4ff2-bd8c-473fd41e54bf.html",
    # EVENT_RSVP_NOTIFICATION variables EVENT_NAME, PERSON_INFORMATION, MANAGE_EVENT_LINK
    "EVENT_RSVP_NOTIFICATION": "https://mosaico.jlm2017.fr/emails/6f2eb6f0-cf59-4e2e-ab62-a8d204c6166b.html",
    # EVENT_RSVP_CONFIRMATION variables EVENT_NAME  EVENT_SCHEDULE CONTACT_NAME CONTACT_EMAIL LOCATION_NAME LOCATION_ADDRESS EVENT_LINK
    "EVENT_RSVP_CONFIRMATION": "https://mosaico.jlm2017.fr/emails/71fa1bc8-1b94-4d88-98dc-27c5502b83f8.html",
    # EVENT_CANCELLATION variables: EVENT_NAME
    "EVENT_CANCELLATION": "https://mosaico.jlm2017.fr/emails/94c7cbb3-afdc-4d14-a07a-cf9503db5b5f.html",
}

EMAIL_FROM = os.environ.get('EMAIL_FROM', 'La France insoumise <noreply@lafranceinsoumise.fr>')

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

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.environ.get('STATIC_ROOT')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "assets")
]

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'components/',
        'STATS_FILE': os.path.join(STATICFILES_DIRS[0], 'components', 'webpack-stats.json'),
    }
}

MEDIA_URL = '/media/'

MEDIA_ROOT = os.environ.get('MEDIA_ROOT', 'media')

# Authentication

AUTH_USER_MODEL = 'authentication.Role'

AUTHENTICATION_BACKENDS = [
    # Rules permission backend MUST be in first position
    'clients.authentication.AccessTokenRulesPermissionBackend',
    # This backend is necessary to enforce database permissions
    'django.contrib.auth.backends.ModelBackend',
]

if ENABLE_API:
    # This backend is used to connect to the administration panel
    AUTHENTICATION_BACKENDS.append('people.backend.PersonBackend')

if ENABLE_FRONT:
    AUTHENTICATION_BACKENDS.extend([
        # This backend is used for OAuth connection
        'front.backend.OAuth2Backend',
        # This backend is used for connection through links found in emails
        'front.backend.MailLinkBackend'
    ])

# Admin

DAS_ALLOWED_AJAX_SEARCH_PATHS = [
    ('people', 'person', 'location_zip'),
    ('people', 'person', 'location_city'),
    ('groups', 'supportgroup', 'location_city'),
    ('groups', 'supportgroup', 'location_city'),
    ('events', 'event', 'location_city'),
    ('events', 'event', 'location_city'),
]

OTP_TOTP_ISSUER = 'api.lafranceinsoumise.fr'

# REST_FRAMEWORK

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        *(['rest_framework.renderers.BrowsableAPIRenderer'] if DEBUG else []),
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
LOG_DISABLE_JOURNALD = os.environ.get('LOG_DISABLE_JOURNALD', '').lower() in ['y', 'yes', 'true']

if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'journald': {
                'level': 'DEBUG',
                'class': 'systemd.journal.JournaldLogHandler' if not LOG_DISABLE_JOURNALD else 'logging.StreamHandler',
            }
        },
        'loggers': {
            'django.template': {
                'handlers': ['journald'],
                'level': 'INFO',
                'propagate': False,
            },
            'django': {
                'handlers': ['journald'],
                'level': 'DEBUG',
                'propagate': True
            },
            'celery': {
                'handlers': ['journald'],
                'level': 'DEBUG',
                'propagate': True,
            }
        }
    }

# CACHING
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('CACHING_REDIS_URL', 'redis://localhost?db=0'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "caching_"
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

# CELERY
CELERY_BROKER_URL = os.environ.get('BROKER_URL', 'redis://')
# make sure celery does not mess with the root logger
CELERY_WORKER_HIJACK_ROOT_LOGGER = False
# enable worker events to allow monitoring
CELERY_WORKER_SEND_TASK_EVENTS = True
# enable task events to allow monitoring
CELERY_TASK_SEND_SENT_EVENT = True

OAUTH = {
    'client_id': os.environ.get('OAUTH_CLIENT_ID', 'api_front'),
    'client_secret': os.environ.get('OAUTH_CLIENT_SECRET', 'incredible password'),
    'authorization_url': os.environ.get('OAUTH_AUTHORIZATION_URL', 'http://localhost:4002/autoriser'),
    'token_exchange_url': os.environ.get('OAUTH_TOKEN_URL', 'http://localhost:4002/token'),
    'redirect_domain': os.environ.get('OAUTH_REDIRECT_DOMAIN', 'http://localhost:8000'),
    'logoff_url': os.environ.get('OAUTH_LOGOFF_URL', 'http://localhost:4002/deconnexion'),
}

DEFAULT_EVENT_IMAGE = "front/images/default_event_pic.jpg"

PHONENUMBER_DEFAULT_REGION = 'FR'

CONNECTION_LINK_VALIDITY = 7

# allow insecure transports for OAUTHLIB in DEBUG mode
if DEBUG:
    os.environ.setdefault('OAUTHLIB_INSECURE_TRANSPORT', 'y')

# Get the promo
PROMO_CODE_KEY = os.environb.get(b'PROMO_CODE_KEY', b'prout')
PROMO_CODE_TAG = os.environ.get('PROMO_CODE_TAG', 'Code promo matériel')


# HTML settings
USER_ALLOWED_TAGS = [
    'a', 'abbr', 'acronym', 'b', 'br', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'p', 'strong', 'ul', 'h2', 'h3', 'h4'
]
ADMIN_ALLOWED_TAGS = USER_ALLOWED_TAGS + ['table', 'tr', 'td', 'th']

SITE_ID = 1

FILE_UPLOAD_PERMISSIONS = 0o644
