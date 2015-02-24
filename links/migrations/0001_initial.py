# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MusicLinks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bandcamp', models.CharField(max_length=200, verbose_name='bandcamp', blank=True)),
                ('itunes', models.CharField(max_length=200, verbose_name='itunes', blank=True)),
                ('spotify', models.CharField(max_length=200, verbose_name='spotify', blank=True)),
                ('soundcloud', models.CharField(max_length=200, verbose_name='soundcloud', blank=True)),
                ('profile', models.OneToOneField(related_name='music_links', null=True, blank=True, to='artist.ArtistProfile', verbose_name='profile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SocialLinks',
            fields=[
                ('profile', models.OneToOneField(related_name='social_links', primary_key=True, serialize=False, to='accounts.Profile', verbose_name='profile')),
                ('facebook', models.CharField(max_length=200, verbose_name='facebook', blank=True)),
                ('google_plus', models.CharField(max_length=200, verbose_name='google plus', blank=True)),
                ('instagram', models.CharField(max_length=200, verbose_name='instagram', blank=True)),
                ('tumblr', models.CharField(max_length=200, verbose_name='tumblr', blank=True)),
                ('twitter', models.CharField(max_length=200, verbose_name='twitter', blank=True)),
                ('youtube', models.CharField(max_length=200, verbose_name='youtube', blank=True)),
                ('vimeo', models.CharField(max_length=200, verbose_name='vimeo', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
