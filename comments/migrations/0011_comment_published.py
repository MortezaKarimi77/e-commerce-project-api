# Generated by Django 4.2.4 on 2023-10-02 14:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("comments", "0010_remove_comment_published_alter_comment_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="published",
            field=models.BooleanField(default=True, verbose_name="وضعیت انتشار"),
        ),
    ]