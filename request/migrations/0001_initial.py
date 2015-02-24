# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '__first__'),
        ('threads', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedule', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('approved', models.NullBooleanField(default=None, verbose_name='approved')),
                ('applicant', models.ForeignKey(verbose_name='requester', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PrivateRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.ForeignKey(verbose_name='dateRange', to='schedule.DateRange')),
                ('thread', models.OneToOneField(related_name='request', null=True, blank=True, to='threads.Thread', verbose_name='thread')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PublicRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('accept_by', models.DateField(null=True, verbose_name='accept_by', blank=True)),
                ('details', models.TextField(verbose_name='description')),
                ('fulfilled', models.BooleanField(default=False, verbose_name='fulfilled')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NumberOfApplicants',
            fields=[
                ('public_request', models.OneToOneField(related_name='applicants', primary_key=True, serialize=False, to='request.PublicRequest', verbose_name='public_request')),
                ('left', models.PositiveSmallIntegerField(verbose_name='total_bands')),
                ('total', models.PositiveSmallIntegerField(verbose_name='number_of_bands')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RequestParticipant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=1, verbose_name='role', choices=[(b'h', 'Headliner'), (b'o', 'Openers'), (b'v', 'Venue')])),
                ('accepted', models.NullBooleanField(default=None, verbose_name='approved')),
                ('participant', models.ForeignKey(related_name='request_participant', to='threads.Participant')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='publicrequest',
            name='date',
            field=models.ForeignKey(verbose_name='dateRange', to='schedule.DateRange'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publicrequest',
            name='requester',
            field=models.ForeignKey(verbose_name='requester', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publicrequest',
            name='zip_code',
            field=models.ForeignKey(verbose_name='Zipcode', to='contact.Zipcode'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='public_request',
            field=models.ForeignKey(related_name='applications', verbose_name='public_request', to='request.PublicRequest'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='thread',
            field=models.OneToOneField(related_name='application', null=True, blank=True, to='threads.Thread', verbose_name='thread'),
            preserve_default=True,
        ),
    ]
