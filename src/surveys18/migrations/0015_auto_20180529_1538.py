# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-29 07:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surveys18', '0014_auto_20180529_1441'),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extra', models.CharField(blank=True, max_length=50, null=True, verbose_name='Extra')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('farm_related_businesses', models.ManyToManyField(related_name='businesses', to='surveys18.FarmRelatedBusiness', verbose_name='Farm Related Business')),
            ],
        ),
        migrations.RemoveField(
            model_name='survey',
            name='farm_related_businesses',
        ),
        migrations.AddField(
            model_name='business',
            name='survey',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='business', to='surveys18.Survey', verbose_name='Survey'),
        ),
    ]