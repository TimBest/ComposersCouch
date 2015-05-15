# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0002_auto_20150313_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artistprofile',
            name='booking_contact',
            field=models.OneToOneField(related_name='bookingContact', null=True, blank=True, to='contact.ContactInfo', verbose_name='bookingContact'),
        ),
        migrations.AlterField(
            model_name='artistprofile',
            name='label_contact',
            field=models.OneToOneField(related_name='labelContact', null=True, blank=True, to='contact.ContactInfo', verbose_name='labelContact'),
        ),
        migrations.AlterField(
            model_name='artistprofile',
            name='management_contact',
            field=models.OneToOneField(related_name='managementContact', null=True, blank=True, to='contact.ContactInfo', verbose_name='managementContact'),
        ),
        migrations.AlterField(
            model_name='artistprofile',
            name='press_contact',
            field=models.OneToOneField(related_name='pressContact', null=True, blank=True, to='contact.ContactInfo', verbose_name='pressContact'),
        ),
        migrations.AlterField(
            model_name='member',
            name='instruments',
            field=models.ManyToManyField(related_name='instrument', verbose_name='instrument', to='artist.Instrument', blank=True),
        ),
    ]
