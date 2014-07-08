from django.conf.urls.defaults import *
from longturn.warcalc.views import *
from longturn.views import *

urlpatterns = patterns('',
	url(r'^$',				warcalc, name='warcalc'),
)
