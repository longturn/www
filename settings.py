from .settings_secret import *

#DEBUG = True
DEBUG = True

ADMINS = (
	('Michal Mazurek', 'akfaew@gmail.com'),
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
)

LOGIN_URL = "/account/login/"
LOGIN_REDIRECT_URL = "/account/profile/"

AUTHENTICATION_BACKENDS = ('longturn.player.backends.GenMD5ModelBackend',)
