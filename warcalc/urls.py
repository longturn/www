from django.conf.urls import *
from longturn.warcalc.views import *
from longturn.views import *

urlpatterns = [
	url(r'^$',				warcalc, name='warcalc'),
]
