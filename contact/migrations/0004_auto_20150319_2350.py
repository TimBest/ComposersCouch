# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0003_auto_20150310_1946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zipcode',
            name='name',
        ),
        migrations.AddField(
            model_name='zipcode',
            name='city',
            field=models.CharField(default=b'city', max_length=180, verbose_name='city'),
            preserve_default=True,
        ),
    ]
