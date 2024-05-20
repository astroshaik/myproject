# Generated by Django 4.2.13 on 2024-05-19 01:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="roomie",
            name="id",
        ),
        migrations.AlterField(
            model_name="roomie",
            name="roomie_id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                ("task_id", models.AutoField(primary_key=True, serialize=False)),
                ("tasks", models.JSONField()),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField()),
                (
                    "roomie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tasks",
                        to="api.roomie",
                    ),
                ),
            ],
        ),
    ]
