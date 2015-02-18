# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_admin', '0005_auto_20150128_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='training_text',
            field=models.CharField(max_length=10000, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='categories',
            name='course_code',
            field=models.CharField(default=b'CD2015-02-18_16:57:58', max_length=40),
            preserve_default=True,
        ),
    ]
