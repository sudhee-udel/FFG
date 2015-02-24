# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_admin', '0011_auto_20150224_0509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='course_code',
            field=models.CharField(default=b'CD2015-02-24_05:27:26', max_length=40),
            preserve_default=True,
        ),
    ]
