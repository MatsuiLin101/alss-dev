# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-04 09:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basefarmers', '0015_auto_20180504_1745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lack',
            name='is_lack',
        ),
    ]
