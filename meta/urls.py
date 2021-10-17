from django.conf.urls import *
from longturn.meta.views import meta, announce, leave

urlpatterns = [
	url(r'^$', meta),
	url(r'^announce$', announce),
	url(r'^leave$', leave),
]
