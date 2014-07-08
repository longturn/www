from django.contrib.auth.models import User
from django import forms
from django.db import models

class WarCalcForm(forms.Form):
	astr = forms.FloatField()
	ahp = forms.FloatField()
	afp = forms.FloatField()
	dstr = forms.FloatField()
	dhp = forms.FloatField()
	dfp = forms.FloatField()

	def clean(self, *args, **kwargs):
		return super(WarCalcForm, self).clean(*args, **kwargs)
