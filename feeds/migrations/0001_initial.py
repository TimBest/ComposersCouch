# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('photos', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('target', models.ForeignKey(related_name='follower_set', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='following_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('local_votes', models.PositiveIntegerField(default=1)),
                ('site_votes', models.PositiveIntegerField(default=1)),
                ('photo', models.ForeignKey(blank=True, to='photos.Image', null=True)),
                ('target', models.ForeignKey(related_name='target_posts', to=settings.AUTH_USER_MODEL)),
                ('track', models.ForeignKey(blank=True, to='tracks.Media', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
