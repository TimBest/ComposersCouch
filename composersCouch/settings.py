"""
Django settings for composersCouch project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, urlparse
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k$s+jts3d$349yo&ojfqo1wvs!f##2w!p&h$4&qd$uz_5&a7%q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DEVELOPMENT = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.gis',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    'autocomplete_light',
    'crispy_forms',
    'compressor',
    'djcelery',
    'embed_video',
    'stream_framework',
    'pagination',
    'social_auth',
    'static_precompiler',

    'accounts',
    'audiofield',
    'annoying',
    'contact',
    'customProfile.fan',
    'customProfile.musician',
    'customProfile.venue',
    'feeds',
    'genres',
    'guardian',
    'photos',
    'progressbarupload',
    'request',
    'schedule',
    'search',
    'sorl.thumbnail',
    'threaded_messages',
    'tracks',
    'userena',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'audiofield.middleware.threadlocals.ThreadLocals',
)

ROOT_URLCONF = 'composersCouch.urls'

WSGI_APPLICATION = 'composersCouch.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# Social Auth
TWITTER_CONSUMER_KEY         = 't64bvuxy0triEzEnHcyg'
TWITTER_CONSUMER_SECRET      = 'jm41BJqDger9veDu3Aa7jswN4ZgQ9yIktlZIY4cSps'
FACEBOOK_APP_ID              = '525965254182714'
FACEBOOK_API_SECRET          = 'bdd9cdd707d80d08bd53660852b91c51'
GOOGLE_OAUTH2_CLIENT_ID      = '566838544572.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET  = 'BpAQ6KT37BLQxNc5ETzC0sMS'

if DEVELOPMENT:
    POSTGIS_VERSION = (2, 1, 4)
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'composerscouchdb',
            'USER': 'postgres',
            'PASSWORD': 'devDatabase', # database Password goes Here
            'HOST': 'localhost',
            'PORT': '',
            'ATOMIC_REQUESTS': True,
        }
    }
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
            'URL': 'http://127.0.0.1:8983/solr',
            'INCLUDE_SPELLING': True,
        },
    }
    # on Heroku redis connection parameters come from environment variables
    redis_url = urlparse.urlparse(os.environ.get('REDISTOGO_URL', 'redis://localhost:6379'))
    STREAM_REDIS_CONFIG = {
        'default': {
            'host': 'localhost',
            'port': 6379,
            'password': '',# Redis Password goes Here
            'db': 0
        },
    }
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }
    # python -m smtpd -n -c DebuggingServer localhost:1025
    MAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_USE_TLS = False
    DEFAULT_FROM_EMAIL = 'testing@example.com'
    """EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp-relay.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'timbest@composerscouch.com'
    EMAIL_HOST_PASSWORD = #password goes here
    DEFAULT_FROM_EMAIL = 'messenger@composerscouch.com'"""

else:
    POSTGIS_VERSION = (2, 1, 1)
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': os.environ['RDS_DB_NAME'],
            'OPTIONS': {
                'options': '-c search_path=gis,public,pg_catalog'
            },
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
            'URL': 'ec2-54-174-202-254.compute-1.amazonaws.com:8983/solr',
            'INCLUDE_SPELLING': True,
        },
    }
    # on Heroku redis connection parameters come from environment variables
    redis_url = urlparse.urlparse(os.environ.get('REDISTOGO_URL', 'aws-my-1pu2uz0351jv0.og7bpd.0001.use1.cache.amazonaws.com:6379'))
    STREAM_REDIS_CONFIG = {
        'default': {
            'host': 'aws-my-1pu2uz0351jv0.og7bpd.0001.use1.cache.amazonaws.com',
            'port': 6379,
            'password': None,# Redis Password goes Here
            'db': 0
        },
    }
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': 'ec2-54-174-202-254.compute-1.amazonaws.com:11211',
        }
    }
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp-relay.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
    DEFAULT_FROM_EMAIL = 'messenger@composerscouch.com'


SITE_ID = 1

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join( BASE_DIR, 'composersCouch/media' )
#MEDIA_ROOT = '/media/timothy/Elements/test/'

MEDIA_URL = '/media/'


#10MB
MAX_AUDIO_UPLOAD_SIZE = "10485760"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = os.path.join( BASE_DIR, 'composersCouch/static/staticfiles/' )

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join( BASE_DIR, 'composersCouch/static' ),

)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'static_precompiler.finders.StaticPrecompilerFinder',
    'compressor.finders.CompressorFinder',

)
STATIC_PRECOMPILER_COMPILERS = (
    'static_precompiler.compilers.LESS',
)
STATIC_PRECOMPILER_OUTPUT_DIR = 'compiled'

# Templates
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
)

FILE_UPLOAD_HANDLERS = (
    "progressbarupload.uploadhandler.ProgressBarUploadHandler",
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
)
PROGRESSBARUPLOAD_INCLUDE_JQUERY = False

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.csrf',
    'django.core.context_processors.request',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'composersCouch.context_processors.now',
    'social_auth.context_processors.social_auth_by_type_backends',
)

# over ride user defaults
ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: "/redirect/%s/" % u.username,
}


# Crispy Form Settings
CRISPY_TEMPLATE_PACK = 'bootstrap3'
CRISPY_FAIL_SILENTLY = not DEBUG

#sorl.thumbnail
THUMBNAIL_DEBUG = DEBUG
THUMBNAIL_BACKEND = 'sorl.thumbnail.base.ThumbnailBackend'
THUMBNAIL_PRESERVE_FORMAT=True
THUMBNAIL_FORMAT = 'PNG'

# feedly
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

import djcelery
djcelery.setup_loader()

try:
    from accounts.userena_settings import *
    from accounts.social_auth_settings import *
    from audiofield.settings import *
    from photos.photos_settings import *
except ImportError:
    pass
