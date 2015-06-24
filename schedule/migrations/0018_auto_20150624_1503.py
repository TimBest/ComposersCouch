# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import object_or_text.fields


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0017_auto_20150623_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='headliner',
            field=object_or_text.fields.ModelField(blank=True, to='artist.ArtistProfile', null=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='venue',
            field=object_or_text.fields.ModelField(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
