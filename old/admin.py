from django.contrib import admin
from longturn.old.models import OldUser, OldGame, OldJoined

class OldGameAdmin(admin.ModelAdmin):
	list_display = ('name', 'mode', 'version', 'admin', 'ranking', 'turn', 'date_started', 'date_ended')
	list_filter = ('version', 'mode', 'ranking')

class OldJoinedAdmin(admin.ModelAdmin):
	list_display = ('user', 'game', 'is_idler', 'is_winner')
	search_fields = ('user', 'game', 'is_idler', 'is_winner')
#	list_filter = ('ishuman',)

admin.site.register(OldGame, OldGameAdmin)
admin.site.register(OldJoined, OldJoinedAdmin)
admin.site.register(OldUser)
