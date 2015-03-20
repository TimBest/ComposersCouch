# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0004_auto_20150319_2350'),
    ]

    operations = [
        migrations.AddField(
            model_name='zipcode',
            name='state',
            field=models.CharField(default=b'', max_length=2, verbose_name='state'),
            preserve_default=True,
        ),
    ]
