# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-04 09:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basefarmers', '0014_auto_20180504_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='lack',
            name='is_lack',
            field=models.BooleanField(default=False, verbose_name='Is Lack'),
        ),
        migrations.AlterField(
            model_name='lack',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Name'),
        ),
    ]
