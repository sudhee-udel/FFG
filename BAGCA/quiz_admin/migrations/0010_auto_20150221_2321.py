# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_admin', '0009_auto_20150219_0104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videos',
            name='name',
        ),
        migrations.AddField(
            model_name='videos',
            name='file',
            field=models.FileField(default='null', upload_to=b'/Users/errang/Desktop/FFG/BAGCA/BAGCA/media/USER_UPLOADED_FILES/', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='videos',
            name='filename',
            field=models.CharField(default='null', max_length=100, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='videos',
            name='url_name',
            field=models.CharField(default='null', max_length=100, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='categories',
            name='course_code',
            field=models.CharField(default=b'CD2015-02-21_23:21:12', max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='videos',
            name='url',
            field=models.URLField(blank=True),
            preserve_default=True,
        ),
    ]
