"""
Django settings for rainmap project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ChangeToUseCrazyCharactersAndSymbolsButKeepLength.'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'djsupervisor',
    'registration',
    'apps.rainmap',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'rainmap.urls'

WSGI_APPLICATION = 'rainmap.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False #True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

# URL prefix for the location that stores the scan results. Make sure to use a
# trailing slash
OUTPUT_URL = "/storage/"
OUTPUT_ROOT = os.path.join(BASE_DIR, "storage")

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'rainmap', 'static'),
)

AUTH_PROFILE_MODULE = 'UserProfile'

### REGISTRATION ###
REGISTRATION_OPEN = True # can new accounts be registered?
ACCOUNT_ACTIVATION_DAYS = 7 # how long before an acct can be activated
LOGIN_REDIRECT_URL = '/'

### EMAIL SETTINGS ###
EMAIL_SUBJECT_PREFIX = '[rainmap]'
EMAIL_USE_TLS = False
EMAIL_HOST = '' # smtp server
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
# Email address shown when sending messages to Users
DEFAULT_FROM_EMAIL = ''
# Email address shown when sending messages to Admins
SERVER_EMAIL = ''

# max size in kB for outgoing attachments
EMAIL_RESULT_LIMIT = 1000

import djcelery
from kombu import Exchange, Queue
djcelery.setup_loader()

CELERYD_CHDIR = BASE_DIR
CELERYD_PID_FILE = os.path.join(BASE_DIR, 'celeryd.pid')
CELERYD_LOG_FILE = os.path.join(BASE_DIR, 'celeryd.log')

BROKER_URL = 'amqp://guest:guest@localhost:5672/'

CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend' #"amqp"
CELERY_IMPORTS = ("apps.rainmap.tasks", )
CELERY_DEFAULT_QUEUE = "default"
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
)
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

## 'process_result' is a wrap-up task that MUST execute on the appserver
CELERY_ROUTES = (
    {"apps.rainmap.tasks.process_result":
        {
            "queue": "default",
        }
    },
)
