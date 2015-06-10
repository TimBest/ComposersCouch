# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='artistprofile',
            options={'ordering': ['-profile__weight']},
        ),
    ]
