# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_admin', '0014_auto_20150224_0533'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='trainer',
            field=models.CharField(default=b'TBD', max_length=100),
            preserve_default=True,
        ),
    ]
