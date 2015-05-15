# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0002_auto_20150315_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='album_art',
            field=models.ForeignKey(related_name='artist_album_art', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='photos.Image', null=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='genre',
            field=models.ManyToManyField(related_name='album_genre', verbose_name='genre', to='genres.Genre', blank=True),
        ),
    ]
