# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('user_data', '0006_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='completed',
            name='date_completed',
            field=models.DateField(default=datetime.date(2015, 2, 24)),
            preserve_default=True,
        ),
    ]
