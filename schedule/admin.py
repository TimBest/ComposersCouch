from django.contrib import admin

from schedule.models import Calendar, Event, Show

class CalendarAdminOptions(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']


admin.site.register(Calendar, CalendarAdminOptions)
admin.site.register(Event)
admin.site.register(Show)
