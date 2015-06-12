# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0006_auto_20150612_1627'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='info',
            name='headliner',
        ),
        migrations.RemoveField(
            model_name='info',
            name='headliner_text',
        ),
        migrations.RemoveField(
            model_name='info',
            name='venue',
        ),
        migrations.RemoveField(
            model_name='info',
            name='venue_text',
        ),
    ]
