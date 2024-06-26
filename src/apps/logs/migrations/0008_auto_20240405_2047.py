# Generated by Django 2.2.24 on 2024-04-05 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0007_auto_20230409_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewlog',
            name='content_type',
            field=models.ForeignKey(limit_choices_to=models.Q(models.Q(('app_label', 'surveys18'), ('model', 'survey')), models.Q(('app_label', 'surveys19'), ('model', 'survey')), models.Q(('app_label', 'surveys20'), ('model', 'survey')), models.Q(('app_label', 'surveys22'), ('model', 'survey')), models.Q(('app_label', 'surveys23'), ('model', 'survey')), models.Q(('app_label', 'surveys24'), ('model', 'survey')), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
    ]
