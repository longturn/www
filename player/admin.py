from django.contrib import admin
from longturn.player.models import Player

class PlayerAdmin(admin.ModelAdmin):
#	list_display = ('nick', 'ishuman')
	search_fields = ('nick',)
#	list_filter = ('ishuman',)

admin.site.register(Player, PlayerAdmin)
