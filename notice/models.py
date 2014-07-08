from django.db import models
from django.contrib.auth.models import User
from longturn.game.models import Game

class Notice(models.Model):
	title = models.CharField(max_length=128)
	notice = models.TextField()
	author = models.ForeignKey(User)
	game = models.ForeignKey(Game, blank=True, null=True)
	pub_date = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return self.title
