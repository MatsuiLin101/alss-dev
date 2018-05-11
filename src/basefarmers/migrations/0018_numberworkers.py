# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-11 03:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basefarmers', '0017_auto_20180511_1120'),
    ]

    operations = [
        migrations.CreateModel(
            name='NumberWorkers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(blank=True, null=True, verbose_name='Value')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('AgeScope', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='age_scope_number_workers', to='basefarmers.AgeScope', verbose_name='Age Scope')),
                ('longterm_for_hire', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='longterm_hire_number_workers', to='basefarmers.LongTermForHire', verbose_name='LongTerm For Hire')),
                ('shortterm_for_hire', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='shortterm_hire_number_workers', to='basefarmers.ShortTermForHire', verbose_name='Shortterm For Hire')),
            ],
            options={
                'verbose_name': 'NumberWorkers',
                'verbose_name_plural': 'NumberWorkers',
            },
        ),
    ]
