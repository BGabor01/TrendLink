from django.dispatch import receiver
from django.db.models.signals import post_save

from apps.connection.models import ConnectionRequest
from apps.connection.models import UserConnection


@receiver(post_save, sender=ConnectionRequest)
def create_connection(sender, instance, **kwargs):
    if instance.status == 1:
        connection_list = UserConnection.objects.get(user=instance.sender)
        connection_list.connections.add(instance.recipient)
