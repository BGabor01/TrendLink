from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from apps.connection.models import UserConnection


@receiver(post_save, sender=User)
def create_profile_and_connection_list(sender, instance, created, **kwargs):
    """
    Signal receiver to create a user profile and connection list when a new User is created.

    Args:
        sender (Model): The model class that sent the signal.
        instance (User): The actual instance being saved.
        created (bool): A boolean indicating if a new record was created.
        **kwargs: Additional keyword arguments.
    """
    from apps.user.models import UserProfile

    if created:
        UserProfile.objects.create(user=instance)
        UserConnection.objects.create(user=instance)
