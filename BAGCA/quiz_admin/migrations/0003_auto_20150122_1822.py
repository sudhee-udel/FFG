# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_admin', '0002_auto_20150113_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='category_description',
            field=models.CharField(default=b'', max_length=1000),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='categories',
            name='course_code',
            field=models.CharField(default=b'CD2015-01-22_18:22:30', max_length=10),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='categories',
            name='due_date',
            field=models.DateField(default=datetime.date.today),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='categories',
            name='duration_hours',
            field=models.DecimalField(default=0.0, max_digits=5, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='categories',
            name='url',
            field=models.URLField(),
            preserve_default=True,
        ),
    ]
