from django.contrib import admin

from tracks import models


admin.site.register(models.Album)
admin.site.register(models.Media)
admin.site.register(models.Track)
