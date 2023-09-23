# Generated by Django 2.2.14 on 2021-11-26 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("surveys19", "0011_stratification"),
    ]

    operations = [
        migrations.AlterField(
            model_name="managementtype",
            name="name",
            field=models.CharField(max_length=50, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="managementtype",
            name="stratify_with",
            field=models.IntegerField(
                choices=[(1, "Field"), (2, "Revenue")], verbose_name="Stratify With"
            ),
        ),
        migrations.AlterField(
            model_name="managementtype",
            name="type",
            field=models.IntegerField(
                choices=[(1, "Crop"), (2, "Animal")], verbose_name="Product Type"
            ),
        ),
    ]
