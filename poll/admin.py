from django.contrib import admin
from longturn.poll.models import Poll, Vote

class PollAdmin(admin.ModelAdmin):
	list_display = ('title', 'game', 'author', 'pub_date', 'end_date', 'valid', 'commited')
	list_filter = ('game', 'author', 'valid', 'commited')

class VoteAdmin(admin.ModelAdmin):
	list_display = ('poll', 'user', 'vote')

admin.site.register(Poll, PollAdmin)
admin.site.register(Vote, VoteAdmin)
