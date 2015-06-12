# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def copy_headliner_and_venue(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Info = apps.get_model("schedule", "Info")
    for info in Info.objects.all():
        info.headliner_test = info.headliner
        info.headliner_test_text = info.headliner_text
        info.venue_test = info.venue
        info.venue_test_text = info.venue_text
        info.save()

def reverse_copy_headliner_and_venue(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Info = apps.get_model("schedule", "Info")
    for info in Info.objects.all():
        info.headliner = info.headliner_test
        info.headliner_text = info.headliner_test_text
        info.venue = info.venue_test
        info.venue_text = info.venue_test_text
        info.save()


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0003_auto_20150515_0038'),
        ('schedule', '0005_auto_20150611_2359'),
    ]

    operations = [
        migrations.RunPython(copy_headliner_and_venue, reverse_copy_headliner_and_venue),
    ]
