#!/usr/bin/python

import sys, os

sys.path.insert(0, "/home/longturn-www")

os.chdir("/home/longturn-www/longturn")
os.environ['DJANGO_SETTINGS_MODULE'] = "longturn.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
