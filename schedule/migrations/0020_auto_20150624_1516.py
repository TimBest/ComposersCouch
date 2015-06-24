# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0019_auto_20150624_1515'),
    ]

    operations = [
        migrations.RenameField(
            model_name='info',
            old_name='headliner_text',
            new_name='headliner',
        ),
        migrations.RenameField(
            model_name='info',
            old_name='venue_text',
            new_name='venue',
        ),
    ]
