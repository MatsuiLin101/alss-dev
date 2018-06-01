# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-21 07:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match', models.BooleanField(default=False, verbose_name='Address Match')),
                ('different', models.BooleanField(default=False, verbose_name='Address Different')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='Address')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'AddressMatch',
                'verbose_name_plural': 'AddressMatch',
            },
        ),
        migrations.CreateModel(
            name='AgeScope',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Name')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'AgeScope',
                'verbose_name_plural': 'AgeScope',
            },
        ),
        migrations.CreateModel(
            name='AnnualIncome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'AnnualIncome',
                'verbose_name_plural': 'AnnualIncomes',
            },
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'Business',
                'verbose_name_plural': 'Business',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(verbose_name='Code')),
                ('name', models.CharField(blank=True, max_length=10, null=True, verbose_name='Name')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'LivestockUnit',
                'verbose_name_plural': 'LivestockUnit',
            },
        ),
        migrations.CreateModel(
            name='CropMarketing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('land_number', models.IntegerField(blank=True, null=True, verbose_name='Land Number')),
                ('land_area', models.IntegerField(blank=True, null=True, verbose_name='Land Area')),
                ('plant_times', models.IntegerField(blank=True, null=True, verbose_name='Plant Times')),
                ('total_yield', models.IntegerField(blank=True, null=True, verbose_name='Total Yield')),
                ('unit_price', models.IntegerField(blank=True, null=True, verbose_name='Unit Price')),
                ('has_facility', models.IntegerField(blank=True, choices=[(0, 'No'), (1, 'Yes')], null=True, verbose_name='Has Facility')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'CropMarketing',
                'verbose_name_plural': 'CropMarketing',
            },
        ),
        migrations.CreateModel(
            name='EducationLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(verbose_name='Code')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Name')),
                ('age', models.IntegerField(blank=True, null=True, verbose_name='Age')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'EducationLevel',
                'verbose_name_plural': 'EducationLevel',
            },
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(verbose_name='Code')),
                ('name', models.CharField(blank=True, max_length=10, null=True, verbose_name='Name')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'Facility',
                'verbose_name_plural': 'Facility',
            },
        ),
        migrations.CreateModel(
            name='FarmerLandArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(blank=True, null=True, verbose_name='Area Value')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'FarmerLandArea',
                'verbose_name_plural': 'FarmerLandArea',
            },
        ),
        migrations.CreateModel(
            name='FarmerLandType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('land_type_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Land Type Name')),
                ('production_type_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Production Type Name')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'FarmerLandType',
                'verbose_name_plural': 'FarmerLandType',
            },
        ),
        migrations.CreateModel(
            name='FarmerWorkDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(verbose_name='Code')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Name')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'FarmerWorkDay',
                'verbose_name_plural': 'FarmerWorkDay',
            },
        ),
        migrations.CreateModel(
            name='FarmRelatedBusiness',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(verbose_name='Code')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Name')),
                ('has_business', models.IntegerField(blank=True, choices=[(0, 'No'), (1, 'Yes')], null=True, verbose_name='Has Business')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'FarmRelatedBusiness',
                'verbose_name_plural': 'FarmRelatedBusiness',
            },
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(verbose_name='Code')),
                ('name', models.CharField(blank=True, max_length=10, null=True, verbose_name='Name')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'Gender',
                'verbose_name_plural': 'Gender',
            },
        ),
        migrations.CreateModel(
            name='IncomeRange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name')),
                ('minimum', models.IntegerField(verbose_name='Minimum Income')),
                ('maximum', models.IntegerField(verbose_name='Maximum Income')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'IncomeRange',
                'verbose_name_plural': 'IncomeRanges',
            },
        ),
        migrations.CreateModel(
            name='Lack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Name')),
                ('is_lack', models.BooleanField(default=False, verbose_name='Is Lack')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'Lack',
                'verbose_name_plural': 'Lack',
            },
        ),
        migrations.CreateModel(
            name='LifeStyle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(verbose_name='Code')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Name')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'LifeStyle',
                'verbose_name_plural': 'LifeStyle',
            },
        ),
        migrations.CreateModel(
            name='LivestockMarketing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raising_number', models.IntegerField(blank=True, null=True, verbose_name='Raising Number')),
                ('total_yield', models.IntegerField(blank=True, null=True, verbose_name='Total Yield')),
                ('unit_price', models.IntegerField(blank=True, null=True, verbose_name='Unit Price')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('contract', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contract', to='surveys18.Contract', verbose_name='Contract')),
            ],
            options={
                'verbose_name': 'LivestockMarketing',
                'verbose_name_plural': 'LivestockMarketing',
            },
        ),
        migrations.CreateModel(
            name='LongTermHire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avg_work_day', models.IntegerField(blank=True, null=True, verbose_name='Average Work Day')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'LongTermHire',
                'verbose_name_plural': 'LongTermHire',
            },
        ),
        migrations.CreateModel(
            name='LongTermLack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(blank=True, null=True, verbose_name='Number Of People')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'LongTermLack',
                'verbose_name_plural': 'LongTermLack',
            },
        ),
        migrations.CreateModel(
            name='Loss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(verbose_name='Code')),
                ('name', models.CharField(blank=True, max_length=10, null=True, verbose_name='Name')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'Loss',
                'verbose_name_plural': 'Loss',
            },
        ),
        migrations.CreateModel(
            name='Management',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'Management',
                'verbose_name_plural': 'Management',
            },
        ),
        migrations.CreateModel(
            name='ManagementType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(verbose_name='Code')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Name')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'ManagementType',
                'verbose_name_plural': 'ManagementType',
            },
        ),
        migrations.CreateModel(
            name='MarketType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'MarketType',
                'verbose_name_plural': 'MarketTypes',
            },
        ),
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name')),
                ('value', models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')])),
            ],
        ),
        migrations.CreateModel(
            name='NoSalaryHire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(blank=True, null=True, verbose_name='Number Of People')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('month', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='surveys18.Month', verbose_name='Month')),
            ],
            options={
                'verbose_name': 'NoSalaryForHire',
                'verbose_name_plural': 'NoSalaryForHire',
            },
        ),
        migrations.CreateModel(
            name='NumberWorkers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('value', models.IntegerField(blank=True, null=True, verbose_name='Value')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('age_scope', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='number_workers', to='surveys18.AgeScope', verbose_name='Age Scope')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'NumberWorkers',
                'verbose_name_plural': 'NumberWorkers',
            },
        ),
        migrations.CreateModel(
            name='OtherFarmWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Name')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'OtherFarmWork',
                'verbose_name_plural': 'OtherFarmWork',
            },
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=100, null=True, verbose_name='Phone')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'Phone',
                'verbose_name_plural': 'Phone',
            },
        ),
        migrations.CreateModel(
            name='Population',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_year', models.IntegerField(blank=True, null=True, verbose_name='Birth Year')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('education_level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='education_level', to='surveys18.EducationLevel', verbose_name='Education Level')),
                ('farmer_work_day', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='farmer_work_day', to='surveys18.FarmerWorkDay', verbose_name='Farmer Work Day')),
                ('gender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relationship', to='surveys18.Gender', verbose_name='Gender')),
                ('life_style', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='life_style', to='surveys18.LifeStyle', verbose_name='Life Style')),
                ('other_farm_work', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='other_farm_work', to='surveys18.OtherFarmWork', verbose_name='Other Farm Work')),
            ],
            options={
                'verbose_name': 'Population',
                'verbose_name_plural': 'Population',
            },
        ),
        migrations.CreateModel(
            name='PopulationAge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_under_15', models.BooleanField(default=False, verbose_name='Is Male')),
                ('count', models.IntegerField(blank=True, null=True, verbose_name='Count')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('gender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys18.Gender', verbose_name='Gender')),
            ],
            options={
                'verbose_name': 'PopulationAge',
                'verbose_name_plural': 'PopulationAge',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Name')),
                ('code', models.CharField(max_length=50, verbose_name='Code')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Product',
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Name')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
        ),
        migrations.CreateModel(
            name='RefuseReason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Name')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'RefuseReason',
                'verbose_name_plural': 'RefuseReason',
            },
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(verbose_name='Code')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Name')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'Relationship',
                'verbose_name_plural': 'Relationship',
            },
        ),
        migrations.CreateModel(
            name='ShortTermHire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avg_work_day', models.IntegerField(blank=True, null=True, verbose_name='Average Work Day')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('month', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='surveys18.Month', verbose_name='Month')),
            ],
            options={
                'verbose_name': 'ShortTermHire',
                'verbose_name_plural': 'ShortTermHire',
            },
        ),
        migrations.CreateModel(
            name='ShortTermLack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(blank=True, null=True, verbose_name='Number Of People')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('months', models.ManyToManyField(related_name='short_term_lacks', to='surveys18.Month', verbose_name='Months')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='short_term_lacks', to='surveys18.Product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'ShortTermLack',
                'verbose_name_plural': 'ShortTermLack',
            },
        ),
        migrations.CreateModel(
            name='Subsidy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_subsidy', models.IntegerField(blank=True, choices=[(0, 'No'), (1, 'Yes')], null=True, verbose_name='Is Subsidy')),
                ('count', models.IntegerField(blank=True, null=True, verbose_name='Number Of People')),
                ('month_delta', models.IntegerField(blank=True, null=True, verbose_name='Month Delta')),
                ('day_delta', models.IntegerField(blank=True, null=True, verbose_name='Day Delta')),
                ('hour_delta', models.IntegerField(blank=True, null=True, verbose_name='Hour Delta')),
                ('remark', models.CharField(blank=True, max_length=100, null=True, verbose_name='Remark')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('reasons', models.ManyToManyField(blank=True, related_name='subsidy', to='surveys18.RefuseReason', verbose_name='subsidies')),
            ],
            options={
                'verbose_name': 'Subsidy',
                'verbose_name_plural': 'Subsidy',
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('farmer_id', models.CharField(max_length=12, verbose_name='Farmer Id')),
                ('farmer_name', models.CharField(blank=True, max_length=10, null=True, verbose_name='Name')),
                ('total_pages', models.IntegerField(verbose_name='Total Pages')),
                ('page', models.IntegerField(verbose_name='Page')),
                ('origin_class', models.IntegerField(blank=True, null=True, verbose_name='Origin Class')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='Address')),
                ('is_hire', models.IntegerField(blank=True, choices=[(0, 'No'), (1, 'Yes')], null=True, verbose_name='Hire')),
                ('note', models.TextField(blank=True, null=True, verbose_name='Note')),
                ('is_updated', models.BooleanField(default=False, verbose_name='Is Updated')),
                ('read_only', models.BooleanField(default=True, verbose_name='Read Only')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Investigation Date')),
                ('distance', models.IntegerField(blank=True, null=True, verbose_name='Investigation Distance(km)')),
                ('period', models.IntegerField(blank=True, null=True, verbose_name='Investigation Period')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('investigator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Investigator')),
                ('lacks', models.ManyToManyField(blank=True, related_name='surveys18', to='surveys18.Lack', verbose_name='Lack')),
            ],
            options={
                'verbose_name': 'Survey',
                'verbose_name_plural': 'Survey',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(verbose_name='Code')),
                ('name', models.CharField(blank=True, max_length=10, null=True, verbose_name='Name')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='surveys18.ProductType', verbose_name='Product Type')),
            ],
            options={
                'verbose_name': 'Unit',
                'verbose_name_plural': 'Unit',
            },
        ),
        migrations.CreateModel(
            name='WorkType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(blank=True, null=True, verbose_name='Code')),
                ('name', models.CharField(blank=True, max_length=30, null=True, verbose_name='Name')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'WorkType',
                'verbose_name_plural': 'WorkType',
            },
        ),
        migrations.AddField(
            model_name='subsidy',
            name='survey',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='subsidy', to='surveys18.Survey', verbose_name='Survey'),
        ),
        migrations.AddField(
            model_name='shorttermlack',
            name='survey',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='short_term_lacks', to='surveys18.Survey', verbose_name='Survey'),
        ),
        migrations.AddField(
            model_name='shorttermlack',
            name='work_types',
            field=models.ManyToManyField(blank=True, related_name='short_term_lacks', to='surveys18.WorkType', verbose_name='Work Types'),
        ),
        migrations.AddField(
            model_name='shorttermhire',
            name='survey',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='short_term_hires', to='surveys18.Survey', verbose_name='Survey'),
        ),
        migrations.AddField(
            model_name='shorttermhire',
            name='work_types',
            field=models.ManyToManyField(blank=True, related_name='short_term_hires', to='surveys18.WorkType', verbose_name='Work Types'),
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='surveys18.ProductType', verbose_name='Product Type'),
        ),
        migrations.AddField(
            model_name='populationage',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='population_ages', to='surveys18.Survey', verbose_name='Survey'),
        ),
        migrations.AddField(
            model_name='population',
            name='relationship',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relationship', to='surveys18.Relationship', verbose_name='Relationship'),
        ),
        migrations.AddField(
            model_name='population',
            name='survey',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='populations', to='surveys18.Survey', verbose_name='Survey'),
        ),
        migrations.AddField(
            model_name='phone',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phones', to='surveys18.Survey', verbose_name='Survey'),
        ),
        migrations.AddField(
            model_name='nosalaryhire',
            name='survey',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='no_salary_hires', to='surveys18.Survey', verbose_name='Survey'),
        ),
        migrations.AddField(
            model_name='management',
            name='survey',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='managements', to='surveys18.Survey', verbose_name='Survey'),
        ),
        migrations.AddField(
            model_name='management',
            name='types',
            field=models.ManyToManyField(related_name='managements', to='surveys18.ManagementType', verbose_name='Types'),
        ),
        migrations.AddField(
            model_name='loss',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='surveys18.ProductType', verbose_name='Product Type'),
        ),
        migrations.AddField(
            model_name='longtermlack',
            name='months',
            field=models.ManyToManyField(related_name='long_term_lacks', to='surveys18.Month', verbose_name='Months'),
        ),
        migrations.AddField(
            model_name='longtermlack',
            name='survey',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='long_term_lacks', to='surveys18.Survey', verbose_name='Survey'),
        ),
        migrations.AddField(
            model_name='longtermlack',
            name='work_type',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='long_term_lacks', to='surveys18.WorkType', verbose_name='Work Type'),
        ),
        migrations.AddField(
            model_name='longtermhire',
            name='survey',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='long_term_hires', to='surveys18.Survey', verbose_name='Survey'),
        ),
        migrations.AddField(
            model_name='longtermhire',
            name='work_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='long_term_hires', to='surveys18.WorkType', verbose_name='Work Type'),
        ),
        migrations.AddField(
            model_name='livestockmarketing',
            name='loss',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='livestock_marketing_loss', to='surveys18.Loss', verbose_name='Loss'),
        ),
        migrations.AddField(
            model_name='livestockmarketing',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='livestock_marketing_product', to='surveys18.Product', verbose_name='Product'),
        ),
        migrations.AddField(
            model_name='livestockmarketing',
            name='survey',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='livestock_marketings', to='surveys18.Survey', verbose_name='Survey'),
        ),
        migrations.AddField(
            model_name='livestockmarketing',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='livestock_marketing_unit', to='surveys18.Unit', verbose_name='Unit'),
        ),
        migrations.AddField(
            model_name='farmerlandarea',
            name='survey',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='farmer_land_areas', to='surveys18.Survey', verbose_name='Survey'),
        ),
        migrations.AddField(
            model_name='farmerlandarea',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='farmer_land_areas', to='surveys18.FarmerLandType', verbose_name='Type'),
        ),
        migrations.AddField(
            model_name='cropmarketing',
            name='loss',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='crop_marketing_loss', to='surveys18.Loss', verbose_name='Loss'),
        ),
        migrations.AddField(
            model_name='cropmarketing',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='surveys18.Product', verbose_name='Product Code'),
        ),
        migrations.AddField(
            model_name='cropmarketing',
            name='survey',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='crop_marketings', to='surveys18.Survey', verbose_name='Survey'),
        ),
        migrations.AddField(
            model_name='cropmarketing',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='crop_marketing_unit', to='surveys18.Unit', verbose_name='Unit'),
        ),
        migrations.AddField(
            model_name='business',
            name='farm_related_businesses',
            field=models.ManyToManyField(related_name='businesses', to='surveys18.FarmRelatedBusiness', verbose_name='Farm Related Business'),
        ),
        migrations.AddField(
            model_name='business',
            name='survey',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='businesses', to='surveys18.Survey', verbose_name='Survey'),
        ),
        migrations.AddField(
            model_name='annualincome',
            name='income_range',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys18.IncomeRange', verbose_name='Income Range'),
        ),
        migrations.AddField(
            model_name='annualincome',
            name='market_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys18.MarketType', verbose_name='Market Type'),
        ),
        migrations.AddField(
            model_name='annualincome',
            name='survey',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='annual_incomes', to='surveys18.Survey', verbose_name='Survey'),
        ),
        migrations.AddField(
            model_name='addressmatch',
            name='survey',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='address_match', to='surveys18.Survey', verbose_name='Survey'),
        ),
    ]