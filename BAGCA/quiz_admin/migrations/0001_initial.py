# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category_text', models.CharField(unique=True, max_length=200)),
                ('category_description', models.CharField(default=b'', max_length=1000)),
                ('trainer', models.CharField(default=b'TBD', max_length=100)),
                ('course_code', models.CharField(default=b'CD', max_length=40)),
                ('due_date', models.DateField(default=datetime.date.today)),
                ('duration_hours', models.DecimalField(default=0.0, max_digits=5, decimal_places=2)),
                ('required_score', models.DecimalField(default=100, max_digits=3, decimal_places=0)),
                ('groups', models.ManyToManyField(related_name='group', to='auth.Group')),
            ],
            options={
                'verbose_name_plural': 'quizzes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url_name', models.CharField(max_length=100, blank=True)),
                ('url', models.URLField(blank=True)),
                ('category_id', models.ForeignKey(to='quiz_admin.Categories')),
            ],
            options={
                'verbose_name_plural': 'content',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=100, blank=True)),
                ('file', models.FileField(upload_to=b'/Users/errang/Desktop/FFG/BAGCA/BAGCA/media/USER_UPLOADED_FILES', blank=True)),
                ('category_id', models.ForeignKey(to='quiz_admin.Categories')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='content',
            name='files',
            field=models.ManyToManyField(to='quiz_admin.Files', blank=True),
            preserve_default=True,
        ),
    ]
