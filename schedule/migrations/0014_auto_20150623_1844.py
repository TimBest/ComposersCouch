# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0013_auto_20150615_1744'),
    ]
    operations = [
        migrations.RenameField(
            model_name='info',
            old_name='headliner',
            new_name='headliner_text',
        ),
        migrations.RenameField(
            model_name='info',
            old_name='venue',
            new_name='venue_text',
        ),
    ]
