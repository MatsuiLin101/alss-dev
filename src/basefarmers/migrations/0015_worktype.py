# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-10 10:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basefarmers', '0014_shorttermforhire'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('shortterm_for_hire', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='shortterm_hire_work_type', to='basefarmers.ShortTermForHire', verbose_name='Shortterm For Hire')),
                ('work_type_code', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='shortterm_hire_work_type_code', to='basefarmers.WorkTypeCode', verbose_name='Work Type Code')),
            ],
            options={
                'verbose_name': 'WorkType',
                'verbose_name_plural': 'WorkType',
            },
        ),
    ]
