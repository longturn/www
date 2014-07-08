from django.db import models
from longturn.game.models import Game, Joined
from datetime import datetime
from django.contrib.auth.models import User

def is_user_in_game(user, game):
	try:
		Joined.objects.get(game=game, user=user)
		return True
	except:
		return False
	return False
	

class Poll(models.Model):
	title		= models.SlugField(max_length=40)
	description	= models.TextField(max_length=8192)
	author		= models.ForeignKey(User)
	game		= models.ForeignKey(Game, blank=True, null=True)
	pub_date	= models.DateTimeField(auto_now_add=True)
	end_date	= models.DateTimeField(blank=True, null=True)
	commited	= models.BooleanField(default=False)
	valid		= models.BooleanField(default=True)
	topic_id	= models.IntegerField(blank=True, null=True, default=0)

	class Meta:
		unique_together = ('title', 'game')

	def has_ended(self):
		return self.end_date < datetime.now()

	def __unicode__(self):
		return "%s/%s" % (self.game, self.title)

VOTE_CHOICES = (
	("For", "For"),
	("Against", "Against"),
	("Withhold", "Withhold"))

class Vote(models.Model):
	poll		= models.ForeignKey(Poll)
	user		= models.ForeignKey(User)
	vote		= models.CharField(max_length=10, choices=VOTE_CHOICES)

	class Meta:
		unique_together = ('poll', 'user')

	def __unicode__(self):
		return "%s/%s" % (self.poll, self.user)

def active_polls(request):
	return {'active_polls': [ p for p in Poll.objects.all() if not p.has_ended() ]}
