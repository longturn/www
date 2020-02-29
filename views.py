from django import forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import Context, TemplateDoesNotExist
from django.template.loader import get_template
from django.conf import settings
import os
import re

import datetime

def about(request, template):
	try:
		return render(request, template)
	except TemplateDoesNotExist:
		raise Http404()

def message(request, emsg):
	return render(request, 'message.html', {'emsg': emsg})

def hello(request):
	return render(request, 'hello.html', { })
