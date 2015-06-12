# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0007_auto_20150612_1706'),
    ]

    operations = [
        migrations.RenameField(
            model_name='info',
            old_name='headliner_test_object',
            new_name='headliner_object',
        ),
        migrations.RenameField(
            model_name='info',
            old_name='headliner_test_text',
            new_name='headliner_text',
        ),
        migrations.RenameField(
            model_name='info',
            old_name='venue_test_object',
            new_name='venue_object',
        ),
        migrations.RenameField(
            model_name='info',
            old_name='venue_test_text',
            new_name='venue_text',
        ),
    ]
