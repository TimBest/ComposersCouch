# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupObjectPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_pk', models.CharField(max_length=255, verbose_name='object ID')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('group', models.ForeignKey(to='auth.Group')),
                ('permission', models.ForeignKey(to='auth.Permission')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserObjectPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_pk', models.CharField(max_length=255, verbose_name='object ID')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('permission', models.ForeignKey(to='auth.Permission')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='userobjectpermission',
            unique_together=set([('user', 'permission', 'object_pk')]),
        ),
        migrations.AlterUniqueTogether(
            name='groupobjectpermission',
            unique_together=set([('group', 'permission', 'object_pk')]),
        ),
    ]
