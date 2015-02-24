# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_admin', '0012_auto_20150224_0527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='course_code',
            field=models.CharField(default=b'CD', max_length=40),
            preserve_default=True,
        ),
    ]
