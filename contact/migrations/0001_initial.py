# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='name')),
                ('phone', models.CharField(max_length=11, verbose_name='phone', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email', blank=True)),
                ('url', models.CharField(max_length=200, verbose_name='website', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact', models.OneToOneField(related_name='contact_info', null=True, blank=True, to='contact.Contact', verbose_name='contact')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address_1', models.CharField(max_length=128, verbose_name='address', blank=True)),
                ('address_2', models.CharField(max_length=128, verbose_name="address cont'd", blank=True)),
                ('city', models.CharField(max_length=64, verbose_name='city', blank=True)),
                ('state', models.CharField(blank=True, max_length=2, verbose_name='state', choices=[(b'AL', 'Alabama'), (b'AK', 'Alaska'), (b'AZ', 'Arizona'), (b'AR', 'Arkansas'), (b'CA', 'California'), (b'CO', 'Colorado'), (b'CT', 'Connecticut'), (b'DE', 'Delaware'), (b'FL', 'Florida'), (b'GA', 'Georgia'), (b'HI', 'Hawaii'), (b'ID', 'Idaho'), (b'IL', 'Illinois'), (b'IN', 'Indiana'), (b'IA', 'Iowa'), (b'KS', 'Kansas'), (b'KY', 'Kentucky'), (b'LA', 'Louisiana'), (b'ME', 'Maine'), (b'MD', 'Maryland'), (b'MA', 'Massachusetts'), (b'MI', 'Michigan'), (b'MN', 'Minnesota'), (b'MS', 'Mississippi'), (b'MO', 'Missouri'), (b'MT', 'Montana'), (b'NE', 'Nebraska'), (b'NV', 'Nevada'), (b'NH', 'New Hampshire'), (b'NJ', 'New Jersey'), (b'NM', 'New Mexico'), (b'NY', 'New York'), (b'NC', 'North Carolina'), (b'ND', 'North Dakota'), (b'OH', 'Ohio'), (b'OK', 'Oklahoma'), (b'OR', 'Oregon'), (b'PA', 'Pennsylvania'), (b'RI', 'Rhode Island'), (b'SC', 'South Carolina'), (b'SD', 'South Dakota'), (b'TN', 'Tennessee'), (b'TX', 'Texas'), (b'UT', 'Utah'), (b'VT', 'Vermont'), (b'VA', 'Virginia'), (b'WA', 'Washington'), (b'WV', 'West Virginia'), (b'WI', 'Wisconsin'), (b'WY', 'Wyoming')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Zipcode',
            fields=[
                ('country', models.CharField(max_length=2, verbose_name='country')),
                ('code', models.CharField(max_length=5, serialize=False, verbose_name='zipcode', primary_key=True)),
                ('name', models.CharField(max_length=180, verbose_name='place name')),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name=b'point')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='location',
            name='zip_code',
            field=models.ForeignKey(verbose_name='zipcode', blank=True, to='contact.Zipcode', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contactinfo',
            name='location',
            field=models.OneToOneField(related_name='contact_info', null=True, blank=True, to='contact.Location', verbose_name='location'),
            preserve_default=True,
        ),
    ]
