from django.conf import settings
from django import forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import F
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
from longturn import nations
import copy
import datetime
import os

def game(request, gamename):
	old = 0
	try:
		game = Game.objects.get(name=gamename)
	except:
		try:
			game = OldGame.objects.get(name=gamename)
			old = 1
		except:
			return message(request, "The game %s does not exist" % gamename)

	joineds = None
	hasjoined = None
	serv = None
	startin = None
	form = None
	delegateform = None
	if not old:
		try:
			hasjoined = Joined.objects.get(game=game, user=request.user)
		except:
			hasjoined = None
		serv = ServGlobalData.objects.filter(game=game)
		if game.date_started:
			startin = game.date_started - datetime.datetime.now()
			startin = startin.days
		else:
			startin = -1

		if request.method == 'POST':
			if 'delegate' in request.POST:
				form = DelegateForm(request.POST)
				if form and form.is_valid():
					regent = request.POST['regent']
					joined = Joined.objects.get(game=game, user=request.user)
					joined.delegation = regent
					joined.save()
				else:
					return message(request, "Player \"%s\" is incorrect." % request.POST['regent'])
			elif 'nodelegate' in request.POST:
				joined = Joined.objects.get(game=game, user=request.user)
				joined.delegation = None
				joined.save()

		joineds = None
		if game.date_started and game.date_started + datetime.timedelta(game.confirm_period) < datetime.datetime.now():
			joineds = list(Joined.objects.filter(game=game, confirmed=True))
			if hasjoined and not hasjoined.confirmed:
				hasjoined = None
		else:
			joineds = list(Joined.objects.filter(game=game))

		if request.method == 'POST' and game.open == True:
			if 'signin' in request.POST:
				form = JoinForm(request.POST)
				if form.is_valid():
					nation = request.POST['nation']
					if nation != 'random':
						for j in joineds:
							if j.user != request.user and j.nation == nation:
								return message(request, "This nation has already been picked by %s" % j.user)

					joined, created = Joined.objects.get_or_create(game=game, user=request.user)
					joined.nation = nation
					joined.save()
					#os.system('%s/join_rate.pl %s' % (settings.PLOT_PATH, gamename))
			elif 'signout' in request.POST:
				form = JoinForm(request.POST)
				if form.is_valid():
					joined = Joined.objects.get(game=game, user=request.user)
					joined.delete()
			elif 'confirm' in request.POST:
				joined = Joined.objects.get(game=game, user=request.user)
				joined.confirmed = True
				joined.save()

			return HttpResponseRedirect("/game/%s/" % gamename)
		else:
			if hasjoined != None:
				nation = hasjoined.nation
				regent = hasjoined.delegation
			else:
				nation = 'random'
				regent = ''

			form = JoinForm(
				initial={
					'game': gamename,
					'nation': nation,
				})
			delegateform = DelegateForm(
				initial={
					'regent': regent,
				})
		for j in joineds:
			if j.nation != "random":
				j.flag = nations.flags[j.nation]
			else:
				j.flag = 'unknown'
		#joineds.sort(key=lambda x: x.user.username.lower(), reverse=False)
		joineds.sort(key=lambda x: x.date_joined, reverse=False)
	else:
		joineds = list(OldJoined.objects.filter(game=game))
                nation = None

	return render(
                request,
		'games/game.html',
		{
			'game': game,
			'joineds': joineds,
			'hasjoined': hasjoined,
			'flag': nations.flags[nation] if nation in nations.flags and nation != 'random' else 'unknown',
			'nation': nation,
			'serv': serv,
			'startin': startin,
			'form': form,
			'delegateform': delegateform,
			'old': old,
		})

def players_txt(request, gamename):
	try:
		game = Game.objects.get(name=gamename)
	except:
		return message(request, "The game %s does not exist" % gamename)

	joineds = list(Joined.objects.filter(game=game))
	joineds.sort(key=lambda x: x.date_joined, reverse=False)

	return render(
                request,
		'games/players.txt',
		{
			'game': game,
			'joineds': joineds,
		},
		content_type='text/text')

def game_list(request):
	games = list(Game.objects.all().order_by(
		F('date_created').desc(nulls_last=True),
		F('date_started').desc(nulls_last=True),
		F('date_ended').desc(nulls_last=True),
		F('version').desc(nulls_last=True)))
	games += list(OldGame.objects.all().order_by(
		F('date_started').desc(nulls_last=True),
		F('date_ended').desc(nulls_last=True),
		F('version').desc(nulls_last=True)))
	return render(
		request,
                'games/game_list.html',
		{
			'games': games,
		})

def nations_v(request):
	nations_list = copy.copy(nations.nations)
	nations_list.remove('random')
	return render(
                request,
		'games/nations.html',
		{
                    'flags': {nation: nations.flags[nation] for nation in nations_list},
		})
