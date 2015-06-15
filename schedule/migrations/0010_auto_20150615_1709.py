# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0009_auto_20150612_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='headliner_temp',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='info',
            name='headliner_temp_is_model',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='info',
            name='venue_temp',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='info',
            name='venue_temp_is_model',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
