from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from core.cache_key_schema import single_user, users_pattern

User = get_user_model()


@receiver(signal=post_save, sender=User)
@receiver(signal=post_delete, sender=User)
def clear_user_cache(instance, **kwargs):
    user = instance
    cache.delete(key=single_user(user.username))
    cache.delete_pattern(pattern=users_pattern())
