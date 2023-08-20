from django import forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import Context, TemplateDoesNotExist
from django.template.loader import get_template
from django.conf import settings
from longturn.game.models import Game, Joined
from longturn.player.forms import *
from longturn.player.models import Player
from longturn.views import message
from longturn.main.misc import *
import hashlib
import datetime

@login_required
def myprofile(request):
	maxdate = datetime.datetime(datetime.MAXYEAR, 1, 1)
	joineds = list(Joined.objects.filter(user=request.user))
	joineds.sort(key=lambda x: x.game.date_started or maxdate, reverse=True)

	if request.method == 'POST':
		if 'profile' in request.POST:
			form = ProfileForm(request.POST)
			if form.is_valid():
				password = request.POST['password']
				email = request.POST['email']
				discord = request.POST['discord']
				info = request.POST['info']

				user = request.user;
				if password != '':
					user.set_password(password)
					user.profile.pass_md5 = hashlib.md5(password.encode()).hexdigest()
					user.profile.pass_sha1 = hashlib.sha1(password.encode()).hexdigest()
				user.email = email
				user.profile.discord = discord
				user.profile.info = info
				user.profile.save()
				user.save()
				return HttpResponseRedirect("/account/profile")
	else:
		form = ProfileForm(
			initial={
				'email': request.user.email,
				'discord': request.user.profile.discord,
				'info': request.user.profile.info
			})

	return render(
                request,
		"registration/myprofile.html",
		{
			'form': form,
			'joineds': joineds,
		})

@login_required
def profile(request, username):
	maxdate = datetime.datetime(datetime.MAXYEAR, 1, 1)
	try:
		player = User.objects.get(username=username)
	except:
		player = None
	joineds = list(Joined.objects.filter(user=player))
	joineds += getoldjoineds(player)
	olduser = getolduser(player)

	joineds.sort(key=lambda x: x.game.date_started or maxdate, reverse=True)

	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			body = request.POST['message']
			send_mail(
				'[longturn] %s, a message from %s!' % (player, request.user),
				body + "\n\n--------\nThis message was sent using the longturn.net contact form.",
				request.user.email,
				[player.email],
				fail_silently=False)
			send_mail(
				'[longturn] Your message to %s has been sent' % (player),
				body + "\n\n--------\nKeep in mind %s might have given a fake address for some reason, so don't rely on it." % (player),
				request.user.email,
				[request.user.email],
				fail_silently=False)
			return message(request, "Message to %s has been sent" % player)
	else:
		form = ContactForm()

	return render(
                request,
		"registration/profile.html",
		{
			'olduser': olduser,
			'form': form,
			'player': player,
			'joineds': joineds,
			'username': username,
		})

def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			email = request.POST['email']
			user = User.objects.create_user(username, email, password)
			user.is_active = True
			user.save()
			user.profile.pass_md5 = hashlib.md5(password.encode()).hexdigest()
			user.profile.pass_sha1 = hashlib.sha1(password.encode()).hexdigest()
			user.profile.save()

			auser = auth.authenticate(username=username, password=password)
			auth.login(request, auser)
			return HttpResponseRedirect("/account/profile/")
	else:
		form = RegistrationForm()

	return render(
                request,
		"registration/register.html",
		{
			'form': form,
		})

def players(request, sort):
	reverse = False
	if sort[0] == 'x':
		reverse = True
		sort = sort[1:]

	players = list(User.objects.all())
	if sort == 'username':
		players.sort(key=lambda x: x.username.lower(), reverse=reverse)
	elif sort == 'admin':
		players.sort(key=lambda x: x.is_staff, reverse=reverse)

	return render(
                request,
		"registration/players.html",
		{
			'players': players,
		})
