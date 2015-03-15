# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0002_auto_20150313_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seating',
            name='seating_chart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='seating chart', blank=True, to='photos.Image', null=True),
            preserve_default=True,
        ),
    ]
