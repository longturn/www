from django.conf.urls import *
#from django.contrib import admin
from django.contrib.auth.views import login, logout
from longturn.game.views import nations_v
from longturn.views import *

#admin.autodiscover()

urlpatterns = [
	url(r'^$',				hello, name='hello'),
	url(r'^intro/$',			about, { 'template': 'intro.html' }, name='intro'),
	url(r'^rules/$',			about, { 'template': 'rules.html' }, name='rules'),
	url(r'^lw_rules/$',			about, { 'template': 'lw-rules.html' }, name='lw_rules'),
	url(r'^contact/$',			about, { 'template': 'contact.html' }, name='contact'),
	url(r'^tech/comps/$',			about, { 'template': 'tech/comps.html' }, name='tech_comps'),
	url(r'^tech/src/$',			about, { 'template': 'tech/src.html' }, name='tech_src'),
	url(r'^nations/$',			nations_v, name='nations'),
	url(r'^screenshots/$',			about, { 'template': 'screenshots.html' }, name='screenshots'),
	url(r'^account/',			include('longturn.player.urls')),
	url(r'^game/',				include('longturn.game.urls')),
	url(r'^warcalc/',			include('longturn.warcalc.urls')),
	url(r'^ranking/',			include('longturn.ranking.urls')),
#	url(r'^admin/',				include(admin.site.urls)),
]
