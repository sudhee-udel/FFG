# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user_data', '0009_auto_20150227_0359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completed',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
