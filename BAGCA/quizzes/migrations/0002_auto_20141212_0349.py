# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='votes',
        ),
        migrations.AddField(
            model_name='choice',
            name='answer',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
