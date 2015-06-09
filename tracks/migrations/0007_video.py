# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import embed_video.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracks', '0006_auto_20150604_1856'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'untitled', max_length=128, verbose_name='Title')),
                ('video', embed_video.fields.EmbedVideoField(help_text=b'Link to youtube or vimeo', verbose_name='Video Link')),
                ('user', models.ForeignKey(related_name='videos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
