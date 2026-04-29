from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile
from finance.default_categories import (
    create_default_categories_for_user,
    create_default_wallets_for_user,
)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        create_default_categories_for_user(instance)
        create_default_wallets_for_user(instance)
