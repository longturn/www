from psycopg2.extensions import AsIs
from django import forms
from django.contrib.auth.models import User
from django.core import validators
from django.db import models
from django.db.models.signals import post_save
from django.db import connections, transaction
import datetime

class Player(models.Model):
	user		= models.OneToOneField(User, related_name="profile")
	info		= models.TextField(max_length=8192, blank=True, null=True)
	pass_md5	= models.CharField(max_length=64)
	pass_sha1	= models.CharField(max_length=64)

	def __unicode__(self):
		return self.user.username

	def forum_account(self):
		try:
			cursor = connections['fluxbb'].cursor()

			cursor.execute("SELECT id,username FROM users WHERE username = '%s'", [ AsIs(self.user) ])
			nick = cursor.fetchone()
		except:
			nick = None
		return nick

	def create_forum_account(self):
		if self.forum_account() != None:
			return False
		try:
			cursor = connections['fluxbb'].cursor()

			cmd = 'INSERT INTO users (username, group_id, password, email, email_setting, timezone, dst, language, style) '
			vals = "VALUES('%s', 4, '%s', '%s', 1, 0, 0, 'English', 'Longturn')"
			cursor.execute(cmd + vals, [AsIs(self.user), AsIs(self.pass_md5), AsIs(self.user.email)])
			transaction.commit_unless_managed(using='fluxbb')
			ret = True
		except:
			ret = False
		return ret
		
	def update_forum_account(self):
		if self.forum_account() == None:
			return False
		try:
			cursor = connections['fluxbb'].cursor()

			cmd = "UPDATE users SET password='%s', email='%s' WHERE username='%s'"
			cursor.execute(cmd, [AsIs(self.pass_sha1), AsIs(self.user.email), AsIs(self.user)])
			transaction.commit_unless_managed(using='fluxbb')
			ret = True
		except:
			ret = False
		return ret

	class Meta:
		ordering = ['user']


def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Player.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)
