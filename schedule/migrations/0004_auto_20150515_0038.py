# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_auto_20150315_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='openers',
            field=models.ManyToManyField(related_name='shows_opening', to='artist.ArtistProfile', blank=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='poster',
            field=models.ForeignKey(related_name='event_poster', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='photos.Image', null=True),
        ),
    ]
