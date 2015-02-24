# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('genres', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='popular',
            field=models.BooleanField(default=False, verbose_name='popular'),
            preserve_default=True,
        ),
    ]
