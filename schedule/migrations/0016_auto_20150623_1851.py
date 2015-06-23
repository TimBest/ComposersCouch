# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def copy_headliner_and_venue(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Info = apps.get_model("schedule", "Info")
    for info in Info.objects.all():
        if info.headliner_is_model:
            info.headliner_id = info.headliner_text
        if info.venue_is_model:
            info.venue_id = info.venue_text
        info.save()

def reverse_copy_headliner_and_venue(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Info = apps.get_model("schedule", "Info")
    for info in Info.objects.all():
        if info.headliner_id:
            info.headliner_is_model = True
        else:
            info.headliner_is_model = False
        if info.venue_id:
            info.venue_is_model = True
        else:
            info.venue_is_model = False
        info.save()

class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0003_auto_20150515_0038'),
        ('schedule', '0015_auto_20150623_1850'),
    ]

    operations = [
        migrations.RunPython(copy_headliner_and_venue, reverse_copy_headliner_and_venue),
    ]
