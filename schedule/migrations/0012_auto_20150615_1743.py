# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0011_auto_20150615_1723'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='info',
            name='headliner_object',
        ),
        migrations.RemoveField(
            model_name='info',
            name='headliner_text',
        ),
        migrations.RemoveField(
            model_name='info',
            name='venue_object',
        ),
        migrations.RemoveField(
            model_name='info',
            name='venue_text',
        ),
    ]
