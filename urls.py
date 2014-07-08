from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.generic.simple import direct_to_template
from longturn.game.views import nations_v
from longturn.views import *

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$',				hello, name='hello'),
	url(r'^intro/$',			about, { 'template': 'intro.html' }, name='intro'),
	url(r'^rules/$',			about, { 'template': 'rules.html' }, name='rules'),
	url(r'^contact/$',			about, { 'template': 'contact.html' }, name='contact'),
	url(r'^tech/comps/$',			about, { 'template': 'tech/comps.html' }, name='tech_comps'),
	url(r'^tech/src/$',			about, { 'template': 'tech/src.html' }, name='tech_src'),
	url(r'^nations/$',			nations_v, name='nations'),
	url(r'^screenshots/$',			about, { 'template': 'screenshots.html' }, name='screenshots'),
	(r'^account/',				include('longturn.player.urls')),
	(r'^game/',				include('longturn.game.urls')),
	(r'^poll/',				include('longturn.poll.urls')),
	(r'^warcalc/',				include('longturn.warcalc.urls')),
	(r'^ranking/',				include('longturn.ranking.urls')),
	(r'^admin/',				include(admin.site.urls)),
)
