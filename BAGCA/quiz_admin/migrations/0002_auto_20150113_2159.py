# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('quiz_admin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='groups',
            field=models.ManyToManyField(related_name='group', to='auth.Group'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='categories',
            name='category_text',
            field=models.CharField(unique=True, max_length=200),
            preserve_default=True,
        ),
    ]
