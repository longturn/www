import os
import sys

sys.path.append('/home/longturn-www/')

os.environ['PYTHON_EGG_CACHE'] = '/home/longturn-www/.python-egg'
os.environ['DJANGO_SETTINGS_MODULE'] = 'longturn.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
