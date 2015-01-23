# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_admin', '0003_auto_20150122_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='required_score',
            field=models.DecimalField(default=100, max_digits=3, decimal_places=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='categories',
            name='course_code',
            field=models.CharField(default=b'CD2015-01-22_18:30:01', max_length=10),
            preserve_default=True,
        ),
    ]
