# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_data', '0003_userassignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='completed',
            name='category_text',
            field=models.CharField(default='remove me', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='completed',
            name='category',
            field=models.ForeignKey(to='quiz_admin.Categories'),
            preserve_default=True,
        ),
    ]
