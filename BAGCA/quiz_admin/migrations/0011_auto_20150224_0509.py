# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_admin', '0010_auto_20150221_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='course_code',
            field=models.CharField(default=b'CD2015-02-24_05:08:55', max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='videos',
            name='file',
            field=models.FileField(upload_to=b'/Users/errang/Desktop/FFG/BAGCA/BAGCA/media/USER_UPLOADED_FILES', blank=True),
            preserve_default=True,
        ),
    ]
