# Generated by Django 5.0.2 on 2024-03-26 13:54

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("category", models.CharField(default=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Product",
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
                (
                    "name",
                    models.CharField(
                        default=False,
                        max_length=255,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Product name can only contain letters, numbers, spaces, '?', '!', ',', '.', hyphens, and apostrophe characters.",
                                regex="^[A-Za-z0-9?!,.\\'\\s-]+$",
                            )
                        ],
                    ),
                ),
                ("description", models.TextField()),
                ("image", models.ImageField(default="", upload_to="Product")),
                ("price", models.IntegerField(default=0)),
                ("size", models.CharField(default="", max_length=50)),
                (
                    "category",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="home.category",
                    ),
                ),
            ],
        ),
    ]
