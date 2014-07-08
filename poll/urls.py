from django.conf.urls.defaults import *
from longturn.poll.views import *
from longturn.views import *

urlpatterns = patterns('',
	url(r'^$',				poll_list, {'sort': "title"}, name='poll_list'),
	url(r'^sort/(\w+)/$',			poll_list, name='poll_list'),
	url(r'^([0-9]+)/$',			poll, name='poll'),
	url(r'^create/$',			new_poll, name='new_poll'),
)
