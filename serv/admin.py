from django.contrib import admin
from longturn.serv.models import *

class ServUserDataAdmin(admin.ModelAdmin):
	list_display = ('game', 'turn', 'user')

class ServGlobalDataAdmin(admin.ModelAdmin):
	list_display = ('game', 'turn')

admin.site.register(ServGlobalData, ServGlobalDataAdmin)
admin.site.register(ServUserData, ServUserDataAdmin)
