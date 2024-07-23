from django.db.models.signals import post_save
from django.dispatch import receiver

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from apps.connection.models import ConnectionRequest, UserConnection


@receiver(post_save, sender=ConnectionRequest)
def create_connection_and_send_signal(sender, instance, **kwargs):
    """
    Handles the post-save signal for ConnectionRequest model.

    Sends notifications and updates connection lists based on the status of the connection request.

    Args:
        sender (Model): The model class that sent the signal.
        instance (ConnectionRequest): The actual instance being saved.
        **kwargs: Additional keyword arguments.
    """
    channel_layer = get_channel_layer()
    match instance.status:
        case 0:
            async_to_sync(channel_layer.group_send)(
                f"user_{instance.recipient.id}",
                {
                    "type": "notification_message",
                    "message": f"{instance.sender} wants to connect with you!",
                },
            )
        case 1:
            connection_list = UserConnection.objects.get(user=instance.sender)
            connection_list.connections.add(instance.recipient)
            async_to_sync(channel_layer.group_send)(
                f"user_{instance.sender.id}",
                {
                    "type": "notification_message",
                    "message": f"{instance.recipient} accepted your connection request!",
                },
            )
        case 2:
            async_to_sync(channel_layer.group_send)(
                f"user_{instance.sender.id}",
                {
                    "type": "notification_message",
                    "message": f"{instance.recipient} rejected your connection request!",
                },
            )
