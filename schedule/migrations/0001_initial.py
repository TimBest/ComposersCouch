# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0001_initial'),
        ('contact', '__first__'),
        ('threads', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('slug', models.SlugField(max_length=200, verbose_name='slug')),
                ('owner', models.OneToOneField(related_name='calendar', verbose_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'calendar',
                'verbose_name_plural': 'calendar',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DateRange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField(verbose_name='start')),
                ('end', models.DateTimeField(help_text='The end time must be later than the start time.', verbose_name='end')),
            ],
            options={
                'verbose_name': 'dateRange',
                'verbose_name_plural': 'dateRanges',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('approved', models.BooleanField(default=False, verbose_name='approved')),
                ('visible', models.BooleanField(default=False, verbose_name='visible')),
            ],
            options={
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('headliner_text', models.CharField(max_length=255, null=True, blank=True)),
                ('openers_text', models.CharField(max_length=255, null=True, blank=True)),
                ('venue_text', models.CharField(max_length=255, null=True, blank=True)),
                ('headliner', models.ForeignKey(related_name='shows_headlining', blank=True, to='artist.ArtistProfile', null=True)),
                ('location', models.ForeignKey(related_name='event_location', blank=True, to='contact.Location', null=True)),
                ('openers', models.ManyToManyField(related_name='shows_opening', null=True, to='artist.ArtistProfile', blank=True)),
                ('poster', models.ForeignKey(related_name='event poster', blank=True, to='photos.Image', null=True)),
                ('venue', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'info',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('current', models.OneToOneField(related_name='line', primary_key=True, serialize=False, to='schedule.Event', verbose_name='current_event')),
                ('line', django.contrib.gis.db.models.fields.LineStringField(srid=4326, null=True, verbose_name=b'line', blank=True)),
                ('next', models.OneToOneField(related_name='pervious_line', null=True, blank=True, to='schedule.Event', verbose_name='next_event')),
            ],
            options={
                'verbose_name': 'line',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('approved', models.NullBooleanField(default=None, verbose_name='approved')),
                ('visible', models.BooleanField(default=False, verbose_name='visible')),
                ('turnout', models.IntegerField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.ForeignKey(related_name='show', verbose_name='date', to='schedule.DateRange')),
                ('info', models.ForeignKey(related_name='show', verbose_name='Info', to='schedule.Info')),
                ('thread', models.OneToOneField(related_name='show', null=True, blank=True, to='threads.Thread', verbose_name='messages')),
            ],
            options={
                'verbose_name': 'show',
                'verbose_name_plural': 'shows',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='calendar',
            field=models.ForeignKey(related_name='events', verbose_name='calendar', to='schedule.Calendar'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='show',
            field=models.ForeignKey(related_name='events', verbose_name='show', to='schedule.Show'),
            preserve_default=True,
        ),
    ]
