# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('user_data', '0007_completed_date_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completed',
            name='date_completed',
            field=models.DateField(default=datetime.date(2015, 2, 27)),
            preserve_default=True,
        ),
    ]
