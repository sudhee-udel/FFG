# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_admin', '0004_auto_20150122_1830'),
    ]

    operations = [
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('category_id', models.ForeignKey(to='quiz_admin.Categories')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='categories',
            options={'verbose_name_plural': 'quizzes'},
        ),
        migrations.RemoveField(
            model_name='categories',
            name='url',
        ),
        migrations.AlterField(
            model_name='categories',
            name='course_code',
            field=models.CharField(default=b'CD2015-01-28_19:34:38', max_length=40),
            preserve_default=True,
        ),
    ]
