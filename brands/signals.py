import shutil
from pathlib import Path

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Brand


@receiver(signal=pre_delete, sender=Brand)
def delete_brand_media_directory(instance, **kwargs):
    brand = instance
    if brand.main_image:
        directory = Path(brand.main_image.path).parent
        shutil.rmtree(path=directory, ignore_errors=True)
