from django.contrib.auth.models import User
from django import forms
from longturn.player.models import Player
from longturn.game.models import Game
from django.forms.widgets import RadioSelect
from django.db import models
import datetime

VOTE_CHOICES = (
	("For", "For"),
	("Against", "Against"),
	("Withhold", "Withhold"))

class VoteForm(forms.Form):
	vote = forms.ChoiceField(widget=RadioSelect, choices=VOTE_CHOICES)

	def clean(self, *args, **kwargs):
		return super(VoteForm, self).clean(*args, **kwargs)

class NewVoteForm(forms.Form):
	title = forms.SlugField(max_length=40, help_text='only letters, digits, hyphens and underscores')
	description = forms.CharField(
		widget=forms.Textarea(),
		max_length=8192,
		help_text='Some HTML is accepted: p, i, b, strong, u, h1, h2, h3, pre, tt, br, hr'
	)
	game = forms.ChoiceField(choices=[(g, g) for g in Game.objects.filter(date_ended = None)] + [("General", "General")])
	topic_id = forms.IntegerField(
		required=False,
		label='Topic ID',
		help_text='Enter only if a forum topic related to the poll already exists. Enter the topic_id, you can get it from the URL of the topic. For example, for <tt>.../viewtopic.php?id=10</tt> enter 10. Leave this value blank and a new topic will be created automatically.'
		)
	file = forms.FileField(required=False)

	def clean(self, *args, **kwargs):
		return super(NewVoteForm, self).clean(*args, **kwargs)
