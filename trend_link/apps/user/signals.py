from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    from apps.user.models import UserProfile

    if created:
        UserProfile.objects.create(user=instance)
