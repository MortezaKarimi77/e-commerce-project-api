# Generated by Django 4.2.4 on 2023-08-17 20:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("categories", "0002_category_full_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="full_name",
            field=models.CharField(max_length=255, verbose_name="نام"),
        ),
    ]
