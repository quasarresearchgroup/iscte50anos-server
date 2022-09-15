from django.contrib import admin

from events.models import Event


class EventAdmin(admin.ModelAdmin):
    list_filter = [
        "scope"
    ]
    search_fields = ['title', 'topics__title']


admin.site.register(Event, EventAdmin)

