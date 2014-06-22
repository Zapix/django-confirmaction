from django.contrib import admin

from . import models


class ActionAdmin(admin.ModelAdmin):
    list_display = ('user_contact', 'action_func', 'get_kwargs',
                    'get_action_status_display',
                    'created', 'executed', 'result', 'live_time')
    search_fields = ('user_contact', 'action_func')
    list_filter = ('action_status', )
admin.site.register(models.Action, ActionAdmin)
