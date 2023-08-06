import os

from .settings_secret import *

#DEBUG = True
DEBUG = False

ADMINS = (
	('The Lonturn Team', 'longturn-net@gmail.com'),
)

MANAGERS = ADMINS

# DATABASES from settings_secret

APPEND_SLASH = True
TIME_ZONE = 'Europe/Warsaw'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
MEDIA_ROOT = '/home/longturn-www/media/'
MEDIA_URL = '/media/'
STATIC_ROOT = '/home/longturn-www/longturn/static/'
STATIC_URL = '/static/'
PLOT_PATH = '/home/longturn-www/longturn/plots/'
ADMIN_MEDIA_PREFIX = '/media/'
# SECRET_KEY from settings_secret

MIDDLEWARE = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
#	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'longturn.urls'

#ALLOWED_HOSTS = ['localhost']
ALLOWED_HOSTS = ['longturn.net', 'www.longturn.net']

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'OPTIONS': {
        'context_processors': [
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.debug',
#            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
#            'django.template.context_processors.tz',
            'django.contrib.messages.context_processors.messages',
            'longturn.main.models.paths',
            'longturn.main.models.active_games',
        ],
        'loaders': [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
#           'django.template.loaders.app_directories.load_template_source',
#           'django.template.loaders.eggs.Loader',
        ]
    },
    'DIRS': [
        './longturn/templates',
	'/home/longturn-www/longturn/templates',
    ]
}]

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
#	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.admin',
	'django.contrib.admindocs',
	'django.contrib.humanize',
	'longturn.main',
	'longturn.player',
	'longturn.game',
	'longturn.warcalc',
	'longturn.serv',
	'longturn.fluxbb',
	'longturn.old',
    'oauth2_provider',
)

LOGIN_URL = "/account/login/"
LOGIN_REDIRECT_URL = "/account/profile/"

AUTHENTICATION_BACKENDS = ('longturn.player.backends.GenMD5ModelBackend',)

# For OAuth
SCOPES = {"user": "User information"}
REFRESH_TOKEN_EXPIRE_SECONDS = 3600 * 24 * 7
if "OIDC_KEY" in os.environ:
    OAUTH2_PROVIDER = {
        "OIDC_ENABLED": True,
        "OIDC_RSA_PRIVATE_KEY": os.environ["OIDC_KEY"],
        "OAUTH2_VALIDATOR_CLASS": "longturn.oauth_validator.LongturnOAuth2Validator",
        "SCOPES": {
            "openid": "OpenID Connect scope",
        },
    }
