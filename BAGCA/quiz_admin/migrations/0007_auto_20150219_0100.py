# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_admin', '0006_auto_20150218_1657'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categories',
            name='training_text',
            ),
        migrations.AlterField(
            model_name='categories',
            name='course_code',
            field=models.CharField(default=b'CD2015-02-19_01:00:54', max_length=40),
            preserve_default=True,
        ),
    ]
