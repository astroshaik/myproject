# Generated by Django 4.2.13 on 2024-05-23 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_rule_allergy"),
    ]

    operations = [
        migrations.CreateModel(
            name="Allergy",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="", max_length=255)),
                ("description", models.TextField()),
                ("roomie_ids", models.JSONField()),
            ],
        ),
        migrations.RemoveField(
            model_name="rule",
            name="allergy",
        ),
        migrations.AddField(
            model_name="roomie",
            name="name",
            field=models.CharField(default="", max_length=255),
        ),
    ]
