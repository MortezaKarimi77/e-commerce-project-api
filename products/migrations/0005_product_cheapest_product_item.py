# Generated by Django 4.2.4 on 2023-08-24 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0004_alter_productitem_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="cheapest_product_item",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="cheapest_product",
                to="products.productitem",
                verbose_name="ارزان\u200cترین محصول",
            ),
        ),
    ]