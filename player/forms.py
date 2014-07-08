from django import forms
from django.contrib.auth.models import User
from django.core import validators
from django.db import models
from django.db.models.signals import post_save

class UserField(forms.CharField):
	def clean(self, value):
		super(UserField, self).clean(value)
		try:
			User.objects.get(username=value)
			raise forms.ValidationError("Someone is already using this username. Please pick a different one.")
		except User.DoesNotExist:
			return value

class RegistrationForm(forms.Form):
	username = UserField(
		max_length=30,
		validators=[
			validators.RegexValidator(
				regex='^[a-zA-Z0-9_]+$',
				message='use only characters from the class [a-zA-Z0-9_]'
			)
		],
		help_text='only characters from the class [a-zA-Z0-9_] allowed, max_length=30. Players will need to type your nick to communicate with you, so make it simple.')
	email = forms.EmailField(
		max_length=60,
		help_text='communication is very important in Longturn. Be sure to enter an address you actually check. Messages from other users, as well as notifications about game start will be sent to this address. You can leave this value blank for now and change it later. It will not be verified.',
		required=False)
	password = forms.CharField(
		widget=forms.PasswordInput(),
		max_length=60,
		min_length=5,
		help_text="don't use a valuable password you use somewhere else.",
		label="Password")
	password2 = forms.CharField(
		widget=forms.PasswordInput(),
		max_length=60,
		min_length=5,
		label="Repeat password")
	test = forms.CharField(
		max_length=60,
		help_text='Human test: what is the release year of Freeciv? (check <a href="http://en.wikipedia.org/wiki/Freeciv">wikipedia</a>)')

	def clean_password(self):
		if self.data['password'] != self.data['password2']:
			raise forms.ValidationError('Passwords are not the same')
		return self.data['password']
    
	def clean_test(self):
		if not 'test' in self.data:
			raise forms.ValidationError('Incorrect field.')
		if self.data['test'] != '1996':
			raise forms.ValidationError('Incorrect release year. Enter 4 digits.')
		return self.data['test']
    
	def clean(self, *args, **kwargs):
		self.clean_password()
		self.clean_test()
		return super(RegistrationForm, self).clean(*args, **kwargs)

class ProfileForm(forms.Form):
	email = forms.EmailField(
		max_length=60,
		help_text='communication is very important in Longturn. Be sure to enter an address you actually check. Messages from other users, as well as notifications about game start will be sent to this address. You can leave this value blank for now and change it later. It will not be verified.',
		required=False)
	password = forms.CharField(
		widget=forms.PasswordInput(),
		max_length=60,
		min_length=5,
		required=False,
		label='Password',
		help_text='Enter only, if you want to change it.')
	password2 = forms.CharField(
		widget=forms.PasswordInput(),
		max_length=60,
		min_length=5,
		required=False,
		label='Repeat password')
#	notify_new = forms.BooleanField(
#		required=False,
#		label='Creation notify',
#		help_text='Send an email if a new game is created.')
#	notify_start = forms.BooleanField(
#		required=False,
#		label='Start notify',
#		help_text='Send an email if a new game will start soon.')
	info = forms.CharField(
		widget=forms.Textarea(),
		max_length=8192,
		required=False,
		help_text='Additional contact information etc.')

	def clean_password(self):
		if self.data['password'] == '':
			return
		if self.data['password'] != self.data['password2']:
			raise forms.ValidationError('Passwords are not the same')
		return
    
	def clean(self, *args, **kwargs):
		self.clean_password()
		return super(ProfileForm, self).clean(*args, **kwargs)

class ContactForm(forms.Form):
	message = forms.CharField(
		widget=forms.Textarea(),
		max_length=8192,
		required=False)

