# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import object_or_text.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('artist', '0003_auto_20150515_0038'),
        ('schedule', '0014_auto_20150623_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='headliner',
            field=models.ForeignKey(blank=True, to='artist.ArtistProfile', null=True),
        ),
        migrations.AddField(
            model_name='info',
            name='venue',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='headliner_text',
            field=object_or_text.fields.ModelOrTextField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='venue_text',
            field=object_or_text.fields.ModelOrTextField(max_length=255, null=True),
        ),
    ]
