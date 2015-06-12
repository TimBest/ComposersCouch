# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0008_auto_20150612_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='headliner_object',
            field=models.ForeignKey(related_name='shows_headlining_object', verbose_name='headliner_object', blank=True, to='artist.ArtistProfile', null=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='headliner_text',
            field=models.CharField(max_length=255, null=True, verbose_name='headliner_text', blank=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='venue_object',
            field=models.ForeignKey(related_name='shows_hosting_object', verbose_name='venue_object', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='venue_text',
            field=models.CharField(max_length=255, null=True, verbose_name='venue_text', blank=True),
        ),
    ]
