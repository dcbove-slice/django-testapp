# Generated by Django 5.0.7 on 2025-01-07 21:16

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Shape",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("face_count", models.IntegerField(max_length=3)),
                ("is_sharp", models.BooleanField()),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("updated_date", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
