from django import forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import Context, TemplateDoesNotExist
from django.template import RequestContext
from django.template.loader import get_template
from django.views.generic.simple import direct_to_template
from django.conf import settings
import os
import re

import datetime

def about(request, template):
	try:
		return render_to_response(template, context_instance=RequestContext(request))
	except TemplateDoesNotExist:
		raise Http404()

def message(request, emsg):
	return render_to_response('message.html', {'emsg': emsg}, context_instance=RequestContext(request))

def hello(request):
	return render_to_response('hello.html', { }, context_instance=RequestContext(request))
