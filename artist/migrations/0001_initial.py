# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '__first__'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtistProfile',
            fields=[
                ('profile', models.OneToOneField(related_name='artist_profile', primary_key=True, serialize=False, to='accounts.Profile', verbose_name='profile')),
                ('name', models.CharField(max_length=64, verbose_name='band name')),
                ('biography', models.TextField(null=True, verbose_name='biography', blank=True)),
                ('booking_contact', models.ForeignKey(related_name='bookingContact', null=True, blank=True, to='contact.ContactInfo', unique=True, verbose_name='bookingContact')),
                ('label_contact', models.ForeignKey(related_name='labelContact', null=True, blank=True, to='contact.ContactInfo', unique=True, verbose_name='labelContact')),
                ('management_contact', models.ForeignKey(related_name='managementContact', null=True, blank=True, to='contact.ContactInfo', unique=True, verbose_name='managementContact')),
                ('press_contact', models.ForeignKey(related_name='pressContact', null=True, blank=True, to='contact.ContactInfo', unique=True, verbose_name='pressContact')),
            ],
            options={
                'abstract': False,
                'permissions': (('view_profile', 'Can view profile'),),
            },
            bases=('accounts.profile',),
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='name')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='name')),
                ('current_member', models.BooleanField(default=True, verbose_name='is current member')),
                ('biography', models.TextField(null=True, verbose_name='biography', blank=True)),
                ('instruments', models.ManyToManyField(related_name='instrument', null=True, verbose_name='instrument', to='artist.Instrument', blank=True)),
                ('profile', models.ForeignKey(related_name='members', blank=True, to='artist.ArtistProfile', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
