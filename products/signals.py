import shutil
from pathlib import Path

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Product, ProductMedia


@receiver(signal=pre_delete, sender=Product)
def delete_product_media_directory(instance, **kwargs):
    product = instance
    if product.main_image:
        directory = Path(product.main_image.path).parent
        shutil.rmtree(path=directory, ignore_errors=True)


@receiver(signal=pre_delete, sender=ProductMedia)
def delete_product_media_file(instance, **kwargs):
    product_media_file = instance.file
    product_media_file.delete(save=False)
