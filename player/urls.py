from django.conf.urls import *
from django.contrib.auth.views import login, logout
from longturn.player.views import *

from longturn.views import *

urlpatterns = patterns('',
	url(r'^login/$',			login, name='login'),
	url(r'^logout/$',			logout, name='logout'),
	url(r'^register/$',			register, name='register'),
	url(r'^profile/$',			myprofile, name='myprofile'),
	url(r'^profile/([a-zA-Z0-9_]+)/$',	profile, name='profile'),
	url(r'^players/$',			players, {'sort': "username"}, name='players'),
	url(r'^players/sort/(\w+)/$',		players, name='players'),
	url(r'^invalid/$',			logout, name='invalid'),
)
