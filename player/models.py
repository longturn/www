from psycopg2.extensions import AsIs
from django import forms
from django.contrib.auth.models import User
from django.core import validators
from django.db import models
from django.db.models.signals import post_save
from django.db import connections, transaction
import datetime

class Player(models.Model):
	user		= models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
	info		= models.TextField(max_length=8192, blank=True, null=True)
	pass_md5	= models.CharField(max_length=64)
	pass_sha1	= models.CharField(max_length=64)
	discord         = models.CharField(max_length=128, blank=True, null=True)

	def __unicode__(self):
		return self.user.username

	class Meta:
		ordering = ['user']


def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Player.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)
