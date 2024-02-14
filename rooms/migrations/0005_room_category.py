# Generated by Django 5.0.2 on 2024-02-14 13:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0001_initial"),
        ("rooms", "0004_alter_amenity_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="categories.category",
            ),
        ),
    ]
