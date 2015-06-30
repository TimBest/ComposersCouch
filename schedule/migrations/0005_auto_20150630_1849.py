# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_auto_20150515_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='venue',
            field=models.ForeignKey(related_name='shows_hosting', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
