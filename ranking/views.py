from django.conf import settings
from django import forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import Context, TemplateDoesNotExist
from django.template.loader import get_template
from longturn.game.models import Game, Joined
from longturn.old.models import OldGame, OldJoined
from longturn.game.forms import JoinForm, DelegateForm
from longturn.views import message
from longturn.player.models import Player
from django.contrib.auth.models import User
from longturn.serv.models import ServGlobalData, ServUserData
from longturn.old.models import OldUser
from longturn.main.misc import *
from longturn import nations
import datetime

def ranking(request):
	users = list(User.objects.all())
	for u in users:
		u.times_played = timesplayed(u)
		#u.times_won = timeswon(u)
	for ouser in OldUser.objects.all():
		if not ouser.activeuser:
			ouser.times_played = oldtimesplayed(ouser)
			#ouser.times_won = oldtimeswon(ouser)
			users.append(ouser)

	return render(
                request,
		'ranking/ranking.html',
		{
			'users': users,
		})
