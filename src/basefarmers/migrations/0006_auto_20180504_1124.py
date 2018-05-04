# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-04 03:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basefarmers', '0005_auto_20180504_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='basefarmer',
            name='read_only',
            field=models.BooleanField(default=True, verbose_name='Read Only'),
        ),
        migrations.AlterField(
            model_name='basefarmer',
            name='page',
            field=models.IntegerField(blank=True, null=True, verbose_name='Page'),
        ),
        migrations.AlterField(
            model_name='basefarmer',
            name='total_pages',
            field=models.IntegerField(blank=True, null=True, verbose_name='Total Pages'),
        ),
    ]
