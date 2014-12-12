# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_admin', '0001_initial'),
        ('quizzes', '0002_auto_20141212_0349'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='category',
            field=models.ForeignKey(default=1, to='quiz_admin.Categories'),
            preserve_default=False,
        ),
    ]
