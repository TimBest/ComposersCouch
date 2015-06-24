# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0018_auto_20150624_1503'),
    ]

    operations = [
        migrations.RenameField(
            model_name='info',
            old_name='headliner',
            new_name='headliner_model',
        ),
        migrations.RenameField(
            model_name='info',
            old_name='venue',
            new_name='venue_model',
        ),
    ]
