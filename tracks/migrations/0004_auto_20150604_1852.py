# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import audiofield.fields
import embed_video.fields
import tracks.models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0003_auto_20150515_0038'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='audio',
            field=audiofield.fields.AudioField(help_text=b'Currently supports mp3 and ogg', upload_to=tracks.models.get_audio_upload_path, null=True, verbose_name='Audio file', blank=True),
        ),
        migrations.AddField(
            model_name='track',
            name='title',
            field=models.CharField(default=b'untitled', max_length=128, verbose_name='Title'),
        ),
        migrations.AddField(
            model_name='track',
            name='video',
            field=embed_video.fields.EmbedVideoField(help_text=b'Link to youtube or vimeo', null=True, verbose_name='Video Link', blank=True),
        ),
    ]
