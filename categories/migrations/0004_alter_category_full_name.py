# Generated by Django 4.2.4 on 2023-08-17 22:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("categories", "0003_alter_category_full_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="full_name",
            field=models.CharField(
                blank=True, editable=False, max_length=255, verbose_name="نام کامل"
            ),
        ),
    ]