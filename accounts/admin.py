from django.contrib import admin

from .models import FanProfile, MusicianProfile, VenueProfile


admin.site.register(FanProfile)
admin.site.register(MusicianProfile)
admin.site.register(VenueProfile)

