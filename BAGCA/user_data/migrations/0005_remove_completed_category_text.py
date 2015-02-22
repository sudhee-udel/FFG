# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_data', '0004_auto_20150221_0223'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='completed',
            name='category_text',
        ),
    ]
