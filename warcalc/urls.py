from django.conf.urls import *
from longturn.warcalc.views import *
from longturn.views import *

urlpatterns = patterns('',
	url(r'^$',				warcalc, name='warcalc'),
)
