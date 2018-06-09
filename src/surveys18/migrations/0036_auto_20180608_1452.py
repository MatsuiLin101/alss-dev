# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-06-08 06:52
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('surveys18', '0035_builderfile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='builderfile',
            name='created',
        ),
        migrations.AddField(
            model_name='builderfile',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2018, 6, 8, 6, 52, 2, 979887, tzinfo=utc), verbose_name='Create Time'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='builderfile',
            name='datafile',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='DataFile'),
        ),
        migrations.AlterField(
            model_name='builderfile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to=settings.AUTH_USER_MODEL, verbose_name='DataFile'),
        ),
    ]