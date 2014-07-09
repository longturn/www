from BeautifulSoup import BeautifulSoup, Comment
from django.template import Library
from django.utils.datastructures import SortedDict
from django.conf import settings
from longturn import nations
register = Library()

@register.filter(name='sanitize')
def sanitize_html(value):
	valid_tags = 'p i b strong u h1 h2 h3 pre tt br hr'.split()
	valid_attrs = ''.split()
	soup = BeautifulSoup(value)
	for comment in soup.findAll(
		text=lambda text: isinstance(text, Comment)):
		comment.extract()
	for tag in soup.findAll(True):
		if tag.name not in valid_tags:
			tag.hidden = True
		tag.attrs = [(attr, val) for attr, val in tag.attrs
					 if attr in valid_attrs]
	return soup.renderContents().decode('utf8').replace('javascript:', '')

@register.filter(name='sort')
def listsort(value):
	if isinstance(value, dict):
		new_dict = SortedDict()
		key_list = value.keys()
		key_list.sort()
		for key in key_list:
			new_dict[key] = value[key]
		return new_dict
	elif isinstance(value, list):
		new_list = list(value)
		new_list.sort()
		return new_list
	else:
		return value
	listsort.is_safe = True

@register.filter(name='flag_url')
def flag_url(value):
	if value != "random":
		f = nations.flags[value]
	else:
		f = 'unknown'
	return '%s/flags/%s.png' % (settings.STATIC_URL, f)

@register.filter(name='shorten')
def shorten(value):
	if len(value) > 7:
		value = value[:7] + "..."
	return value;
