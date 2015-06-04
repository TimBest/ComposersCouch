# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numberofapplicants',
            name='left',
            field=models.PositiveSmallIntegerField(verbose_name='total bands'),
        ),
        migrations.AlterField(
            model_name='numberofapplicants',
            name='total',
            field=models.PositiveSmallIntegerField(verbose_name='number of bands'),
        ),
    ]
