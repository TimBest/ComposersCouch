# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_auto_20150302_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='poster',
            field=models.ForeignKey(related_name='event poster', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='photos.Image', null=True),
            preserve_default=True,
        ),
    ]
