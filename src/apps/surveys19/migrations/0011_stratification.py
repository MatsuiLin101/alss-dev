# Generated by Django 2.2.14 on 2021-10-31 11:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ("surveys19", "0010_auto_20190726_2016"),
    ]

    operations = [
        migrations.AddField(
            model_name="managementtype",
            name="stratify_with",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "Field"), (2, "Revenue")],
                null=True,
                verbose_name="Stratify With",
            ),
        ),
        migrations.AddField(
            model_name="managementtype",
            name="type",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "Crop"), (2, "Animal")],
                null=True,
                verbose_name="Product Type",
            ),
        ),
        migrations.AddField(
            model_name="citytowncode",
            name="region",
            field=models.PositiveIntegerField(
                blank=True,
                choices=[(1, "North"), (2, "Central"), (3, "South"), (4, "East")],
                null=True,
                verbose_name="Region",
            ),
        ),
        migrations.CreateModel(
            name="Stratify",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_hire", models.BooleanField(verbose_name="Is Hire")),
                (
                    "min_field",
                    models.FloatField(blank=True, null=True, verbose_name="Min Field"),
                ),
                (
                    "max_field",
                    models.FloatField(blank=True, null=True, verbose_name="Max Field"),
                ),
                (
                    "min_revenue",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Min Revenue"
                    ),
                ),
                (
                    "max_revenue",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Max Revenue"
                    ),
                ),
                (
                    "code",
                    models.PositiveIntegerField(db_index=True, verbose_name="Code"),
                ),
                (
                    "population",
                    models.PositiveIntegerField(verbose_name="Population(Statistic)"),
                ),
                (
                    "management_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stratifies",
                        to="surveys19.ManagementType",
                        verbose_name="Management Type",
                    ),
                ),
            ],
            options={
                "verbose_name": "Stratify",
                "verbose_name_plural": "Stratify",
            },
        ),
        migrations.CreateModel(
            name="FarmerStat",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "create_time",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="Create Time",
                    ),
                ),
                (
                    "update_time",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="Update Time",
                    ),
                ),
                (
                    "stratify",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="farmer_stats",
                        to="surveys19.Stratify",
                        verbose_name="Stratify",
                    ),
                ),
                (
                    "survey",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="farmer_stat",
                        to="surveys19.Survey",
                        verbose_name="Survey",
                    ),
                ),
            ],
            options={
                "verbose_name": "Farmer Stat",
                "verbose_name_plural": "Farmer Stat",
            },
        ),
    ]
