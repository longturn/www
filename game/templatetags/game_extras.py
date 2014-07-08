from django.template import Library
from django.conf import settings
register = Library()

def graph(value, arg):
	return '<p> <fieldset style="width: 670"> <legend>%s</legend> <img src="%s/plots/%s/%s.svg"> </fieldset> </p>' % (value, settings.MEDIA_URL, arg, value)

register.filter('graph', graph)
