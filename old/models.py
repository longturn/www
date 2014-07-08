from django.db import models
from django.contrib.auth.models import User
	
class OldUser(models.Model):
	username	= models.CharField(max_length=128)
	activeuser	= models.ForeignKey(User, related_name="activeuser", blank=True, null=True)
	def __unicode__(self):
		return self.username

class OldGame(models.Model):
	VERSION_CHOICES = (
		("2.0", "2.0"),
		("2.1", "2.1"),
		("2.2", "2.2"),
	)
	MODE_CHOICES = (
		("team game", "team game"),
		("teamless", "teamless"),
		("lone wolf", "lone wolf"),
		("experimental", "experimental"),
	)
	name		= models.SlugField(max_length=32, primary_key=True)
	descr		= models.TextField(blank=True, null=True)
	mode		= models.CharField(max_length=128, choices=MODE_CHOICES)
	version		= models.CharField(max_length=128, choices=VERSION_CHOICES)
	admin		= models.CharField(max_length=128)
        players		= models.ManyToManyField(OldUser, through='OldJoined', related_name="players")
	turn		= models.IntegerField(default=0)
	date_started	= models.DateTimeField(blank=True, null=True)
	date_ended	= models.DateTimeField(blank=True, null=True)
	ranking		= models.BooleanField(default=True)
	def __unicode__(self):
		return self.name

class OldJoined(models.Model):
	user		= models.ForeignKey(OldUser, related_name="user");
	game		= models.ForeignKey(OldGame)
	is_idler	= models.BooleanField(default=False)
	is_winner	= models.BooleanField(default=False)
