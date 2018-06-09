# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-06-09 07:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys18', '0037_auto_20180608_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landtype',
            name='statuses',
            field=models.ManyToManyField(blank=True, related_name='land_type', to='surveys18.LandStatus', verbose_name='Land Statuses'),
        ),
        migrations.AlterField(
            model_name='longtermlack',
            name='months',
            field=models.ManyToManyField(blank=True, related_name='long_term_lacks', to='surveys18.Month', verbose_name='Months'),
        ),
        migrations.AlterField(
            model_name='shorttermlack',
            name='months',
            field=models.ManyToManyField(blank=True, related_name='short_term_lacks', to='surveys18.Month', verbose_name='Months'),
        ),
    ]
