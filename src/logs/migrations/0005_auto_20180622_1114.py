# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-06-22 03:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0004_remove_reviewlog_skip_errors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewlog',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='review_logs', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]