from django.conf import settings
from longturn.game.models import Game, Joined
from longturn.serv.models import ServGlobalData
import datetime
import time

def paths(request):
	return {
		'STATIC_ROOT': settings.STATIC_ROOT,
		'STATIC_URL': settings.STATIC_URL,
		'MEDIA_ROOT': settings.MEDIA_ROOT,
		'MEDIA_URL': settings.MEDIA_URL,
		'PLOT_PATH': settings.PLOT_PATH,
	}

def active_games(request):
	mindate = datetime.datetime(datetime.MAXYEAR, 1, 1)
	games = [ g for g in Game.objects.all() if g.has_ended() == False ]
	games.sort(key=lambda x: x.date_started or mindate, reverse=False)
	for g in games:
		if g.port:
			g.to = int(round(time.time()))
			g.to += (int(g.port) - (int(g.port) / 10) * 10) * (2 * 60 * 60)
			g.to %= (23 * 60 * 60)
			g.to = (23 * 60 * 60) - g.to
			g.to = "%2d:%02d:%02d" % (g.to / (60*60), (g.to / 60) % 60, g.to % 60)
		else:
			g.to = "-"
		try:
			g.data = ServGlobalData.objects.get(game=g, turn=g.turn)
		except:
			g.so = Joined.objects.filter(game=g).count()
			g.data = None
		if g.date_started:
			g.startin = g.date_started - datetime.datetime.now()
			g.startin = g.startin.days
		else:
			g.startin = -1
		g.confirmed = Joined.objects.filter(confirmed=True, game=g).count()

	return {'active_games': games}
