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
from longturn.views import message
from longturn.poll.models import *
from longturn.poll.forms import *
from longturn.game.models import Joined, Game
from longturn.fluxbb.models import *
from django.conf import settings
from datetime import date, datetime, time, timedelta
import os.path

def poll(request, pollid):
	try:
		poll = Poll.objects.get(id=pollid)
	except:
		return message(request, "The poll %s does not exist" % pollid)
	poll.subject = topic_subject(poll.topic_id)

	if poll.game:
		eligible = Joined.objects.filter(game=poll.game).count()
	else:
		eligible = User.objects.all().count()
	votes = Vote.objects.filter(poll=poll)
	vcnt = { 'For': 0, 'Against': 0, 'Withhold': 0 }
	for v in votes:
		vcnt[v.vote] += 1
	diff = '%s/polls/%s.diff' % (settings.MEDIA_ROOT, pollid)
	if os.path.isfile(diff):
		f = open(diff, "r")
		diff_text = f.read()
		f.close()
		diff = 'polls/%s.diff' % (pollid)
	else:
		diff = None
		diff_text = None


	if request.method == 'POST':
		form = VoteForm(request.POST)
		try:
			Joined.objects.get(game=poll.game, user=request.user)
			can_create = True
		except:
			can_create = False
		if poll.has_ended():
			return message(request, "This poll has ended")
			
		if form.is_valid() and request.POST['vote'] in ('For', 'Against', 'Withhold') and can_create:
			vote, created = Vote.objects.get_or_create(poll=poll, user=request.user)
			if poll.game != None and not is_user_in_game(request.user, poll.game):
				return message(request, "You are not elligible to vote in this poll. Sign up to the game first")
			
			choice = request.POST['vote']
			vote.vote = choice
			vote.save()
			return HttpResponseRedirect("/poll/%s/" % pollid)
	else:
		try:
			vote = Vote.objects.get(poll=poll, user=request.user)
			form = VoteForm(initial={'vote': vote.vote})
		except:
			form = VoteForm()

	return render_to_response(
		'polls/poll.html',
		{
			'poll': poll,
			'diff': diff,
			'diff_text': diff_text,
			'form': form,
			'vcnt': vcnt,
			'total': votes.count(),
			'eligible': eligible,
		},
		context_instance=RequestContext(request))

def save_file(f, pollid):
	if f:
		destination = open('%s/polls/%s.diff' % (settings.MEDIA_ROOT, pollid), 'wb+')
		for chunk in f.chunks():
			destination.write(chunk)
			destination.close()

def new_poll(request):
	if request.method == 'POST':
		form = NewVoteForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				game = Game.objects.get(name=request.POST['game'])
			except:
				game = None
			if 'create' in request.POST:
				try:
					Joined.objects.get(game=game, user=request.user)
				except:
					return message(request, "You need to sign up to %s before you can create polls related to it" % game)
				poll = Poll.objects.create(
					author = request.user,
					end_date = datetime.now() + timedelta(weeks=1),
					title = request.POST['title'],
					description = request.POST['description'],
					game = game)
				if 'file' in request.FILES:
					save_file(request.FILES['file'], poll.id)
				if not request.POST['topic_id']:
					poll.topic_id = new_topic(poll)
				else:
					poll.topic_id = request.POST['topic_id']
				poll.save()
			elif 'preview' in request.POST:
				form = NewVoteForm(
					initial={
						'title': request.POST['title'],
						'description': request.POST['description'],
						'game': game,
					})
				return render_to_response(
					'polls/new_poll.html',
					{
						'description': request.POST['description'],
						'form': form,
					},
					context_instance=RequestContext(request))

			return HttpResponseRedirect("/poll/%s/" % poll.id)
	else:
		form = NewVoteForm()

	return render_to_response(
		'polls/new_poll.html',
		{
			'form': form,
		},
		context_instance=RequestContext(request))


def poll_list(request, sort):
	reverse = False
	if sort[0] == 'x':
		reverse = True
		sort = sort[1:]

	apolls = [p for p in Poll.objects.all() if not p.has_ended() ]
	apolls.sort(key=lambda x: x.pub_date, reverse=True)
	epolls = [p for p in Poll.objects.all() if p.has_ended() ]
	epolls.sort(key=lambda x: x.pub_date, reverse=True)
	for p in epolls:
		f = Vote.objects.filter(poll=p, vote="For").count();
		a = Vote.objects.filter(poll=p, vote="Against").count();
		if f > a:
			p.passed = 1
		else:
			p.passed = 0
		
	return render_to_response(
		'polls/poll_list.html',
		{
			'apolls': apolls,
			'epolls': epolls,
		},
		context_instance=RequestContext(request))
