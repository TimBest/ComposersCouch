# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0005_auto_20150604_1852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='track',
            name='media',
        ),
        migrations.DeleteModel(
            name='Media',
        ),
    ]
