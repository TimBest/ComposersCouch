# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '__first__'),
        ('accounts', '0001_initial'),
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, null=True, verbose_name='name', blank=True)),
                ('quantity', models.CharField(default=b'', choices=[(b'1', '1'), (b'2', '2'), (b'3', '3'), (b'4', '4'), (b'5', '5'), (b'6', '6'), (b'7', '7'), (b'8', '8'), (b'9', '9')], max_length=1, blank=True, null=True, verbose_name='quantity')),
                ('category', models.CharField(default=b'', choices=[(b'Sound', 'Sound'), (b'Effects', 'Effects'), (b'Accessories', 'Accessories')], max_length=11, blank=True, null=True, verbose_name='category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hours',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weekday', models.CharField(help_text='0-6 (0=Monday)', max_length=1, verbose_name='weekday')),
                ('start', models.TimeField(null=True, verbose_name='start', blank=True)),
                ('end', models.TimeField(null=True, verbose_name='end', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Policies',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=64, null=True, verbose_name='title', blank=True)),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Seating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('capacity', models.CharField(max_length=6, null=True, verbose_name='capacity', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job_title', models.CharField(max_length=64, null=True, verbose_name='job title', blank=True)),
                ('biography', models.TextField(null=True, verbose_name='biography', blank=True)),
                ('contact', models.ForeignKey(verbose_name='contact', blank=True, to='contact.Contact', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VenueProfile',
            fields=[
                ('profile', models.OneToOneField(related_name='venueProfile', primary_key=True, serialize=False, to='accounts.Profile', verbose_name='profile')),
                ('name', models.CharField(max_length=64, verbose_name='venue name')),
                ('biography', models.TextField(null=True, verbose_name='biography', blank=True)),
            ],
            options={
                'abstract': False,
                'permissions': (('view_profile', 'Can view profile'),),
            },
            bases=('accounts.profile',),
        ),
        migrations.AddField(
            model_name='staff',
            name='profile',
            field=models.ForeignKey(related_name='staff', verbose_name='venue', to='venue.VenueProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='seating',
            name='profile',
            field=models.OneToOneField(related_name='seating', verbose_name='venue', to='venue.VenueProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='seating',
            name='seating_chart',
            field=models.ForeignKey(verbose_name='seating chart', blank=True, to='photos.Image', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='policies',
            name='profile',
            field=models.ForeignKey(related_name='policies', verbose_name='venue', to='venue.VenueProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hours',
            name='profile',
            field=models.ForeignKey(related_name='hours', verbose_name='venue', to='venue.VenueProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='equipment',
            name='profile',
            field=models.ForeignKey(related_name='equipment', verbose_name='venue', to='venue.VenueProfile'),
            preserve_default=True,
        ),
    ]
