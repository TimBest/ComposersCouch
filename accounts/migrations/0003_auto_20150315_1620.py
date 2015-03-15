# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='mugshot',
            field=models.ForeignKey(related_name='mugshots_profile', on_delete=django.db.models.deletion.SET_NULL, verbose_name='mugshot', blank=True, to='photos.Image', null=True),
            preserve_default=True,
        ),
    ]
