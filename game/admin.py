from django.contrib import admin
from longturn.game.models import Game, Team, Joined

class GameAdmin(admin.ModelAdmin):
	list_display = ('name', 'mode', 'version', 'admin', 'host', 'port', 'date_created', 'date_started', 'date_ended')
	list_filter = ('version', 'mode', 'host')

class JoinedAdmin(admin.ModelAdmin):
	list_display = ('user', 'game', 'nation', 'team')
	search_fields = ('user__username', 'game__name')

admin.site.register(Game, GameAdmin)
admin.site.register(Team)
admin.site.register(Joined, JoinedAdmin)
