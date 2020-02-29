from django.contrib.auth.models import User
from django import forms
from longturn.player.models import Player
from longturn.game.models import Game
from django.db import models
import time
import datetime

class ServUserData(models.Model):
	user		= models.ForeignKey(User, on_delete=models.CASCADE, related_name="statuser")
	game		= models.ForeignKey(Game, on_delete=models.CASCADE, related_name="statgame")
	turn		= models.IntegerField()

	bulbs		= models.IntegerField()
	cities		= models.IntegerField()
	citizens	= models.IntegerField()
	content		= models.IntegerField()
	corruption	= models.IntegerField()
	food		= models.IntegerField()
	gold		= models.IntegerField()
	govt		= models.IntegerField()
	happy		= models.IntegerField()
	idle		= models.IntegerField()
	landarea	= models.IntegerField()
	literacy	= models.IntegerField()
	munits		= models.IntegerField()
	pollution	= models.IntegerField()
	population	= models.IntegerField()
	production	= models.IntegerField()
	score		= models.IntegerField()
	settledarea	= models.IntegerField()
	shields		= models.IntegerField()
	techs		= models.IntegerField()
	trade		= models.IntegerField()
	unhappy		= models.IntegerField()
	units		= models.IntegerField()
	units_built	= models.IntegerField()
	units_killed	= models.IntegerField()
	units_lost	= models.IntegerField()

	class Meta:
		unique_together = ('user', 'game', 'turn')

	def __unicode__(self):
		return "%s/%s/%s" % (self.game, self.turn, self.user)

class ServGlobalData(models.Model):
	game		= models.ForeignKey(Game, on_delete=models.CASCADE, related_name="game")
	turn		= models.IntegerField()

	players		= models.IntegerField()
	alive		= models.IntegerField()
	bulbs		= models.IntegerField()
	cities		= models.IntegerField()
	citizens	= models.IntegerField()
	corruption	= models.IntegerField()
	food		= models.IntegerField()
	gold		= models.IntegerField()
	landarea	= models.IntegerField()
	munits		= models.IntegerField()
	pollution	= models.IntegerField()
	population	= models.IntegerField()
	settled		= models.IntegerField()
	production	= models.IntegerField()
	shields		= models.IntegerField()
	trade		= models.IntegerField()
	units		= models.IntegerField()
	units_built	= models.IntegerField()
	units_killed	= models.IntegerField()
	units_lost	= models.IntegerField()

	class Meta:
		unique_together = ('game', 'turn')

	def __unicode__(self):
		return "%s/%s" % (self.game, self.turn)
