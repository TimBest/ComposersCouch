# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import photos.fields
import photos.utils
import photos.models.bases.image


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=photos.fields.ImageField(upload_to=photos.utils.get_file_path, verbose_name='File', validators=[photos.models.bases.image.validate_file_extension]),
        ),
    ]
