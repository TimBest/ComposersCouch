from django.contrib import admin

from artist import models


admin.site.register(models.ArtistProfile)
admin.site.register(models.Instrument)
admin.site.register(models.Member)
