from django.conf import settings
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
from longturn.game.models import Game, Joined
from longturn.old.models import OldGame, OldJoined
from longturn.game.forms import JoinForm, DelegateForm
from longturn.views import message
from longturn.player.models import Player
from longturn.notice.models import Notice
from longturn.poll.models import Poll, Vote
from django.contrib.auth.models import User
from longturn.serv.models import ServGlobalData, ServUserData
from longturn import nations
import datetime
import os
import md5
import base64

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
	notices = None
	apolls = None
	epolls = None
	hasjoined = None
	serv = None
	startin = None
	form = None
	delegateform = None
	if not old:
		joineds = list(Joined.objects.filter(game=game))
		try:
			hasjoined = Joined.objects.get(game=game, user=request.user)
		except:
			hasjoined = None
		notices = list(Notice.objects.filter(game=game))
		notices.sort(key=lambda x: x.pub_date, reverse=True)
		apolls = [p for p in Poll.objects.filter(game=game) if not p.has_ended() ]
		apolls.sort(key=lambda x: x.end_date, reverse=False)
		epolls = [p for p in Poll.objects.filter(game=game) if p.has_ended() ]
		epolls.sort(key=lambda x: x.end_date, reverse=False)
		for p in epolls:
			f = Vote.objects.filter(poll=p, vote="For").count();
			a = Vote.objects.filter(poll=p, vote="Against").count();
			if f > a:
				p.passed = 1
			else:
				p.passed = 0
		serv = ServGlobalData.objects.filter(game=game)
		if game.date_started:
			startin = game.date_started - datetime.datetime.now()
			startin = startin.days
		else:
			startin = -1

		if request.method == 'POST':
			if 'delegate' in request.POST:
				regent = request.POST['regent']
				joined = Joined.objects.get(game=game, user=request.user)
				joined.delegation = regent
				joined.save()
				os.system('/home/longturn-www/longturn/log delegate %s to %s' % (request.user, regent))
			elif 'nodelegate' in request.POST:
				joined = Joined.objects.get(game=game, user=request.user)
				joined.delegation = None
				joined.save()
				os.system('/home/longturn-www/longturn/log nodelegate %s' % (request.user))

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
					polls = Poll.objects.filter(game=game)
					for p in polls:
						votes = Vote.objects.filter(poll=p, user=request.user)
						for v in votes:
							v.delete()
					joined.delete()
					os.system('%s/join_rate.pl %s' % (settings.PLOT_PATH, gamename))
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

	return render_to_response(
		'games/game.html',
		{
			'game': game,
			'joineds': joineds,
			'notices': notices,
			'apolls': apolls,
			'epolls': epolls,
			'hasjoined': hasjoined,
			'serv': serv,
			'startin': startin,
			'form': form,
			'delegateform': delegateform,
			'old': old,
		},
		context_instance=RequestContext(request))

def game_list(request):
	mindate = datetime.datetime(datetime.MAXYEAR, 1, 1)
	games = list(Game.objects.all()) + list(OldGame.objects.all())
	games.sort(key=lambda x: x.date_started or mindate, reverse=False)
	return render_to_response(
		'games/game_list.html',
		{
			'games': games,
		},
		context_instance=RequestContext(request))

@login_required
def nation(request, agame, auser):
	try:
		game = Game.objects.get(name=agame)
	except:
		return message(request, "The game %s does not exist" % agame)
	try:
		user = User.objects.get(username=auser)
	except:
		return message(request, "The user %s does not exist" % auser)
	try:
		joined = Joined.objects.get(user=user, game=game)
	except:
		return message(request, "The user %s did not play in %s" % (auser, game))

	if request.user != user:
		return message(request, "Only %s can view his stats" % auser)
	hash = base64.b64encode(md5.new("ABsoHCop-%d-%s-%03d" % (user.id, game, game.turn)).digest())
	hash = hash.replace('/', 'x')
	hash = hash.replace('=', '')
	data = "%s,%s,%s" % (game.name, user.id, hash)
	try:
		stats = ServUserData.objects.get(user=user, game=game, turn=game.turn)
	except:
		return message(request, "These stats do not exist")
	govt = stats.govt
	stats.population *= 1000 # for |intword
	if govt == 1:
		govt = 'despotism'
	if govt == 4:
		govt = 'republic'
	if govt == 5:
		govt = 'democracy'
	return render_to_response(
		'games/nation.html',
		{
			'game': game,
			'joined': joined,
			'data': data,
			'govt': govt,
			'stats': stats,
		},
		context_instance=RequestContext(request))

def nations_v(request):
	return render_to_response(
		'games/nations.html',
		{
			'flags': nations.flags,
		},
		context_instance=RequestContext(request))
