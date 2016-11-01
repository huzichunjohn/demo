"""
Django settings for demo project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$qgopm#os1128dd!jypv1-xcpa0d(pmu*tnwj2d^zei&!x^f$x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',
    'debug_toolbar',
    'blog',
    'todo',
    'student',
    'django_extlog',
    'crequest',
    'rest_framework',
    'rest_framework_swagger',
    'rest_framework_docs',
    'rest_framework.authtoken',
    'rest_auth',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'django_extensions',
    'corsheaders',
    'logentry_admin',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'crequest.middleware.CrequestMiddleware',
    'audit_log.middleware.UserLoggingMiddleware',
    'django_extlog.middleware.AuditLoggingMiddleware',
    'demo.middleware.RequestMetricsMiddleware',
)

ROOT_URLCONF = 'demo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR + '/templates/',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog.context_processors.info',
            ],
        },
    },
]

WSGI_APPLICATION = 'demo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'demo',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
#STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, "static"),
#)

LOGIN_REDIRECT_URL = '/blog/'

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]
DEBUG_TOOLBAR_CONFIG = {"JQUERY_URL": "http://code.jquery.com/jquery-2.1.1.min.js"}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_RENDER_CLASSES': ('rest_framework.renders.JSONRender'),
    'PAGE_SIZE': 10,
    'DEFAULT_THROTTLE_CLASSES': (
	'api.throttles.BurstRateThrottle',
	'api.throttles.SustainedRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
	'burst': '60/min',
	'sustained': '1000/day'
    }
}

SWAGGER_SETTINGS = {
    'api_path': '/',
    'is_authenticated': False,
    'is_superuser': False,
}

CRONJOBS = [
    ('*/5 * * * *', 'blog.cron.my_scheduled_job', '>> /tmp/scheduled_job.log'),
    ('*/1 * * * *', 'django.core.management.call_command', ['dumpdata', 'blog'], {'indent': 4}, '> /tmp/blog.json'),
]

SITE_ID = 1

#CACHES = {
#    'default': {
#	'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#	'LOCATION': '127.0.0.1:11211',
#    }
#}

CACHES = {
    'default': {
       'BACKEND': 'django_redis.cache.RedisCache',
       'LOCATION': 'redis://127.0.0.1:6379/1',
       'OPTIONS': {
           'CLIENT_CLASS': 'django_redis.client.DefaultClient',
       },
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'syslog': {
            'level': 'DEBUG',
            'class': 'demo.loggers.SyslogHandler',
        },
    },
    'loggers': {
        'demo': {
            'handlers': ['syslog'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    'localhost',
    'localhost:8080',
)

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept-encoding',
    'accept',
    'cache-control',
    'origin',
    'authorization',
    'x-csrftoken',
    'dnt',
    'access-control-allow-origin'
)

GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}

ADMIN_LOGIN = 'admin'
ADMIN_PASSWORD = 'pbkdf2_sha256$20000$2t8yfDfkiiGe$o5lWDPuT0Z3wRpmYHghL3k36kxhnvwSszK1H9ZqW+K8='

AUTHENTICATION_BACKENDS = ['demo.backends.SettingsBackend', 'django.contrib.auth.backends.ModelBackend']

REST_FRAMEWORK_DOCS = {
    'HIDE_DOCS': os.environ.get('HIDE_DRFDOCS', False)
}

GEOIP_PATH = "/tmp/GeoLiteCity.dat"

import logging
logging.basicConfig(level=logging.INFO)

from metrology import Metrology
from metrology.reporter.logger import LoggerReporter
reporter = LoggerReporter(level=logging.INFO, interval=5)
reporter.start()
