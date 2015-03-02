# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='line',
            name='next',
            field=models.ForeignKey(related_name='pervious_lines', verbose_name='next_event', blank=True, to='schedule.Event', null=True),
            preserve_default=True,
        ),
    ]
