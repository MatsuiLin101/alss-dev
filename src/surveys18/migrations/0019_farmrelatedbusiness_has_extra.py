# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-29 07:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys18', '0018_auto_20180529_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmrelatedbusiness',
            name='has_extra',
            field=models.BooleanField(default=False, verbose_name='Has Extra'),
        ),
    ]
