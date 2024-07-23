from django.dispatch import receiver
from django.db.models.signals import post_save

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from apps.post.models import Like


@receiver(post_save, sender=Like)
def send_like_notification(sender, instance, created, **kwargs):
    """
    Sends a notification when a Like instance is created.

    Args:
        sender (Model): The model class that sent the signal.
        instance (Like): The actual instance being saved.
        created (bool): A boolean indicating if a new record was created.
        **kwargs: Additional keyword arguments.
    """
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{instance.post.user.id}",
            {
                "type": "notification_message",
                "message": f"{instance.user} liked your post!",
            },
        )
