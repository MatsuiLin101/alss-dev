# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-30 09:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surveys18', '0022_auto_20180530_1659'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='refuse',
            name='survey',
        ),
        migrations.AddField(
            model_name='subsidy',
            name='survey',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='subsidy', to='surveys18.Survey', verbose_name='Survey'),
            preserve_default=False,
        ),
    ]
