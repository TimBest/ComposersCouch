# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0012_auto_20150615_1743'),
    ]

    operations = [
        migrations.RenameField(
            model_name='info',
            old_name='headliner_temp',
            new_name='headliner',
        ),
        migrations.RenameField(
            model_name='info',
            old_name='headliner_temp_is_model',
            new_name='headliner_is_model',
        ),
        migrations.RenameField(
            model_name='info',
            old_name='venue_temp',
            new_name='venue',
        ),
        migrations.RenameField(
            model_name='info',
            old_name='venue_temp_is_model',
            new_name='venue_is_model',
        ),
    ]
