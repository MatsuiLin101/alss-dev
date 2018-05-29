# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-29 06:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys18', '0013_auto_20180529_1138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='is_hire',
        ),
        migrations.AddField(
            model_name='survey',
            name='hire',
            field=models.BooleanField(default=False, verbose_name='Hire'),
        ),
        migrations.AddField(
            model_name='survey',
            name='non_hire',
            field=models.BooleanField(default=False, verbose_name='Non Hire'),
        ),
    ]
