# Generated by Django 2.2.2 on 2019-07-26 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("surveys19", "0009_builderfile_delete_exist"),
    ]

    operations = [
        migrations.AlterField(
            model_name="survey",
            name="farmer_id",
            field=models.CharField(
                db_index=True, max_length=12, verbose_name="Farmer Id"
            ),
        ),
    ]
