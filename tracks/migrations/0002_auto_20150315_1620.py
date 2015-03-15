# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='album_art',
            field=models.ForeignKey(related_name='artist Album art', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='photos.Image', null=True),
            preserve_default=True,
        ),
    ]
