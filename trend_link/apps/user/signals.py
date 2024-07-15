from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from apps.connection.models import UserConnection


@receiver(post_save, sender=User)
def create_profile_and_connection_list(sender, instance, created, **kwargs):
    from apps.user.models import UserProfile

    if created:
        UserProfile.objects.create(user=instance)
        UserConnection.objects.create(user=instance)
