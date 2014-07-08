from django.contrib.auth.models import User
from django import forms
from longturn.player.models import Player
from django.db import models
from longturn import nations
from django.conf import settings

class NationField(forms.CharField):
	def clean(self, value):
		super(NationField, self).clean(value)
		if value in nations.nations:
			return value
		else:
			raise forms.ValidationError("The nation \"%s\" does not exist." % value)

class PlayerField(forms.CharField):
	def clean(self, value):
		super(PlayerField, self).clean(value)
		if User.objects.get(username=value):
			return value
		else:
			raise forms.ValidationError("The player \"%s\" does not exist." % value)

class JoinForm(forms.Form):
	nation = NationField(
		max_length=128,
		help_text='Must be a valid nation or the word <tt>random</tt>, see <a href="/nations/">nations</a>.')

	def clean(self, *args, **kwargs):
		return super(JoinForm, self).clean(*args, **kwargs)

class DelegateForm(forms.Form):
	regent = PlayerField(
		max_length=128,
		help_text='Must be an existing player, see <a href="/account/players/">players</a>.')

	def clean(self, *args, **kwargs):
		return super(JoinForm, self).clean(*args, **kwargs)
