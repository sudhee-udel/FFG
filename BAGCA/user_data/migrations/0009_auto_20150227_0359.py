# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_data', '0008_auto_20150227_0356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completed',
            name='date_completed',
            field=models.DateField(),
            preserve_default=True,
        ),
    ]
