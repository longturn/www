from django.conf.urls import *
from longturn.game.views import *
from longturn.views import *

urlpatterns = [
	url(r'^$',				game_list, name='game_list'),
	url(r'^([a-zA-Z0-9]+)/$',		game, name='game'),
	url(r'^([a-zA-Z0-9]+)/players.serv$',	players_serv),
]
