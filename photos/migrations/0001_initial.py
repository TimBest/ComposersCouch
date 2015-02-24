# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
from django.conf import settings
import photos.utils
import photos.models.bases.image


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, null=True, verbose_name='Title', blank=True)),
                ('order', models.IntegerField(default=0, verbose_name='Order')),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=photos.utils.get_file_path, verbose_name='File', validators=[photos.models.bases.image.validate_file_extension])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created', null=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated', null=True)),
                ('user', models.ForeignKey(related_name='images', verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('order', 'id'),
                'abstract': False,
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
                'permissions': (('moderate_images', 'View, update and delete any image'),),
            },
            bases=(models.Model,),
        ),
    ]
