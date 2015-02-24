# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('contact', '__first__'),
        ('genres', '0002_category_popular'),
        ('photos', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('privacy', models.CharField(default=b'open', help_text='Designates who can view your profile.', max_length=15, verbose_name='privacy', choices=[(b'open', 'Open'), (b'registered', 'Registered'), (b'closed', 'Closed')])),
                ('user', models.OneToOneField(related_name='profile', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='user')),
                ('has_owner', models.BooleanField(default=True)),
                ('profile_type', models.CharField(default=b'm', max_length=1, verbose_name='profile type', choices=[(b'f', 'Fan'), (b'm', 'Musician'), (b'v', 'Venue')])),
                ('contact_info', models.OneToOneField(related_name='contactInfo', null=True, blank=True, to='contact.ContactInfo', verbose_name='contactInfo')),
                ('genre', models.ManyToManyField(related_name='genre_artist', null=True, verbose_name='genre', to='genres.Genre', blank=True)),
                ('mugshot', models.ForeignKey(related_name='mugshots_profile', verbose_name='mugshot', blank=True, to='photos.Image', null=True)),
            ],
            options={
                'abstract': False,
                'permissions': (('view_profile', 'Can view profile'),),
            },
            bases=(models.Model,),
        ),
    ]
