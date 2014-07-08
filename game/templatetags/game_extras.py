from django.template import Library
from django.conf import settings
register = Library()

def graph_priv(value, args):
	if args is None:
		return False
	arg_list = [arg.strip() for arg in args.split(',')]
	return '<p> <fieldset style="width: 670"> <legend>%s</legend> <img src="%s/plots/%s/user/%s/%s-%s.svg"> </fieldset> </p>' % (value, settings.MEDIA_URL, arg_list[0], arg_list[1], arg_list[2], value)

def graph(value, arg):
	return '<p> <fieldset style="width: 670"> <legend>%s</legend> <img src="%s/plots/%s/%s.svg"> </fieldset> </p>' % (value, settings.MEDIA_URL, arg, value)

register.filter('graph_priv', graph_priv)
register.filter('graph', graph)
