# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FanProfile',
            fields=[
                ('profile', models.OneToOneField(related_name='fanProfile', primary_key=True, serialize=False, to='accounts.Profile', verbose_name='profile')),
            ],
            options={
                'abstract': False,
                'permissions': (('view_profile', 'Can view profile'),),
            },
            bases=('accounts.profile',),
        ),
    ]
