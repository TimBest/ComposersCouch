# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0016_auto_20150623_1851'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='info',
            name='headliner_is_model',
        ),
        migrations.RemoveField(
            model_name='info',
            name='venue_is_model',
        ),
    ]
