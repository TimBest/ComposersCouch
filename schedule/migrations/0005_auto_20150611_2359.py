# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('artist', '0003_auto_20150515_0038'),
        ('schedule', '0004_auto_20150515_0038'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='headliner_test',
            field=models.ForeignKey(related_name='shows_headlining_test', verbose_name='headliner_test', blank=True, to='artist.ArtistProfile', null=True),
        ),
        migrations.AddField(
            model_name='info',
            name='headliner_test_text',
            field=models.CharField(max_length=255, null=True, verbose_name='headliner_test_text', blank=True),
        ),
        migrations.AddField(
            model_name='info',
            name='venue_test',
            field=models.ForeignKey(related_name='shows_hosting', verbose_name='venue_test', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='info',
            name='venue_test_text',
            field=models.CharField(max_length=255, null=True, verbose_name='venue_test_text', blank=True),
        ),
    ]
