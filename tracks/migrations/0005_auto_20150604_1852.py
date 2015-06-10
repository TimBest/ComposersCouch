# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def copy_media(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Track = apps.get_model("tracks", "Track")
    for track in Track.objects.all():
        track.title = track.media.title
        track.audio = track.media.audio
        track.video = track.media.video
        track.save()

class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0004_auto_20150604_1852'),
    ]

    operations = [
        migrations.RunPython(copy_media),
    ]
