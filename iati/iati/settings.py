# Django settings for iati project.
import sys
import os

def rel(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

sys.path.insert(0, rel('..','lib'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

from local_settings import ADMINS, DATABASES, SERVER_EMAIL, SECRET_KEY

#location of the indexing file for haystack
HAYSTACK_SITECONF = 'iati.search_sites'

#search engine using for Haystack, we use SOLR
HAYSTACK_SEARCH_ENGINE = 'solr'

#where we interface with the solr server
HAYSTACK_SOLR_URL = 'http://127.0.0.1:8080/solr'

SERVER_EMAIL = SERVER_EMAIL

ADMINS = ADMINS

MANAGERS = ADMINS

DATABASES = DATABASES

CACHES = {
    'default' : dict(
        BACKEND = 'johnny.backends.memcached.MemcachedCache',
        LOCATION = ['127.0.0.1:11211'],
        JOHNNY_CACHE = True,
    )
}

JOHNNY_MIDDLEWARE_KEY_PREFIX='jc_oipa'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = rel('../media')
STATIC_ROOT = rel('../static-root')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    rel('../static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = SECRET_KEY

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'johnny.middleware.LocalStoreClearMiddleware',
    'johnny.middleware.QueryCacheMiddleware',
)

ROOT_URLCONF = 'iati.urls'
WSGI_APPLICATION = 'iati.wsgi.application'

TEMPLATE_DIRS = (
    rel('../templates'),
    )


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.static",
    "django.contrib.auth.context_processors.auth",
    "api.context_processor.version",
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'haystack',
    'raven.contrib.django.raven_compat',
    'data',
    'api',
    'tastypie',
    'utils',
    'south',
    'django.contrib.admin',
)

API_VERSION = 'v2.0.1'
API_URL = 'http://127.0.0.1:8080/api/v2'