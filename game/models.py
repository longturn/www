from django import forms
from django.contrib.auth.models import User
from django.db import models
from longturn.player.models import Player
import datetime
import time

class Game(models.Model):
	VERSION_CHOICES = (
		("2.0", "2.0"),
		("2.1", "2.1"),
		("2.2", "2.2"),
		("2.3", "2.3"),
		("2.4", "2.4"),
		("2.5", "2.5"),
		("2.6", "2.6"),
		("2.7", "2.7"),
	)
	MODE_CHOICES = (
		("team game", "team game"),
		("teamless", "teamless"),
		("experimental", "experimental"),
	)
	name		= models.SlugField(max_length=32, primary_key=True)
	descr		= models.TextField()
	mode		= models.CharField(max_length=128, choices=MODE_CHOICES)
	version		= models.CharField(max_length=128, choices=VERSION_CHOICES)
	admin		= models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin", blank=True, null=True)
	players		= models.ManyToManyField(User, through='Joined', related_name="players")
	host		= models.CharField(max_length=128, default="longturn.net", blank=True)
	port		= models.PositiveIntegerField(blank=True, null=True)
	maxplayers	= models.PositiveSmallIntegerField(default=126)
	maxteamsize	= models.PositiveSmallIntegerField(default=5)
	turn		= models.IntegerField(default=0)
	date_created	= models.DateTimeField(auto_now_add=True)
	date_started	= models.DateTimeField(blank=True, null=True)
	date_ended	= models.DateTimeField(blank=True, null=True)
	ranking		= models.BooleanField(default=True)
	open		= models.BooleanField(default=True)
	def has_started(self):
		return self.date_started != None and self.port != None
	def has_ended(self):
		return self.date_ended != None
	def __unicode__(self):
		return self.name

class Team(models.Model):
	name		= models.CharField(max_length=128)
	game		= models.ForeignKey(Game, on_delete=models.CASCADE)
	leader		= models.ForeignKey(User, on_delete=models.CASCADE, related_name="leader")
	members		= models.ManyToManyField(User, through='Joined', related_name="members")

	class Meta:
		unique_together = ('game', 'name')

#	def __unicode__(self):
#		return "%s/%s" % (self.game, self.name)
	def __unicode__(self):
		return "%s" % (self.name)

class Joined(models.Model):
	user		= models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
	date_joined	= models.DateTimeField(auto_now_add=True)
	game		= models.ForeignKey(Game, on_delete=models.CASCADE)
	team		= models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
	nation		= models.CharField(max_length=128, default="random")
	delegation	= models.CharField(default=None, blank=True, null=True, max_length=128)
	is_idler	= models.BooleanField(default=False)
	is_winner	= models.BooleanField(default=False)
	confirmed	= models.BooleanField(default=False)

	class Meta:
		unique_together = ('game', 'user')

	def __unicode__(self):
		return "%s/%s" % (self.game, self.user)
