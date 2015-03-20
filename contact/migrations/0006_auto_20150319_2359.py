# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0005_zipcode_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zipcode',
            name='city',
            field=models.CharField(default=b'', max_length=64, verbose_name='city'),
            preserve_default=True,
        ),
    ]
