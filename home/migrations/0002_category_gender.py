# Generated by Django 5.0.2 on 2024-03-27 08:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="gender",
            field=models.CharField(
                choices=[("M", "Men"), ("W", "Women"), ("K", "Kids")],
                max_length=1,
                null=True,
            ),
        ),
    ]
