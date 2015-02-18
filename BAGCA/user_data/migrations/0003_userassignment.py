# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz_admin', '0006_auto_20150218_1657'),
        ('user_data', '0002_auto_20150128_1934'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.ForeignKey(to='quiz_admin.Categories')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'UserAssignments',
            },
            bases=(models.Model,),
        ),
    ]
