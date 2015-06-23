# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def copy_headliner_and_venue(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Info = apps.get_model("schedule", "Info")
    for info in Info.objects.all():
        if info.headliner_object_id:
            info.headliner_temp = info.headliner_object_id
            info.headliner_temp_is_model = True
        elif info.headliner_text:
            info.headliner_temp = info.headliner_text
            info.headliner_temp_is_model = False
        if info.venue_object_id:
            info.venue_temp = info.venue_object_id
            info.venue_temp_is_model = True
        else:
            info.venue_temp = info.venue_text
            info.venue_temp_is_model = False
        info.save()

def reverse_copy_headliner_and_venue(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Info = apps.get_model("schedule", "Info")
    for info in Info.objects.all():
        if info.headliner_temp_is_model:
            info.headliner_object_id = info.headliner_temp
        else:
            info.headliner_text = info.headliner_temp
        if info.venue_temp_is_model:
            info.venue_object_id = info.venue_temp
        else:
            info.venue_text = info.venue_temp
        info.save()

class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0003_auto_20150515_0038'),
        ('schedule', '0010_auto_20150615_1709'),
    ]

    operations = [
        migrations.RunPython(copy_headliner_and_venue, reverse_copy_headliner_and_venue),
    ]