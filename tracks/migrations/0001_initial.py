# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import embed_video.fields
import audiofield.fields
import tracks.models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0001_initial'),
        ('photos', '0001_initial'),
        ('genres', '0002_category_popular'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('year', models.CharField(max_length=b'4', null=True, verbose_name='Year', blank=True)),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('album_art', models.ForeignKey(related_name='artist Album art', blank=True, to='photos.Image', null=True)),
                ('artist_profile', models.ForeignKey(related_name='albums', blank=True, to='artist.ArtistProfile', null=True)),
                ('genre', models.ManyToManyField(related_name='album_genre', null=True, verbose_name='genre', to='genres.Genre', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('video', embed_video.fields.EmbedVideoField(help_text=b'Link to youtube or vimeo', null=True, verbose_name='Video Link', blank=True)),
                ('audio', audiofield.fields.AudioField(help_text=b'Currently supports mp3 and ogg', upload_to=tracks.models.get_audio_upload_path, null=True, verbose_name='Audio file', blank=True)),
                ('live', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveSmallIntegerField(verbose_name='order')),
                ('album', models.ForeignKey(related_name='track_set', to='tracks.Album')),
                ('media', models.OneToOneField(related_name='album_track', to='tracks.Media')),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
    ]
