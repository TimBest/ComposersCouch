# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='venueprofile',
            options={'ordering': ['-profile__weight']},
        ),
    ]
