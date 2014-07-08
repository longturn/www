from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
from longturn.ranking.views import *
from longturn.views import *

urlpatterns = patterns('',
	url(r'^$',					ranking, name='ranking'),
	#url(r'^([a-zA-Z0-9]+)/$',			game, name='game'),
	#url(r'^([a-zA-Z0-9]+)/([a-zA-Z0-9_-]+)/$',	nation, name='nation'),
)
