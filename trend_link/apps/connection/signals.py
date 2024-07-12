from django.dispatch import receiver
from django.db.models.signals import post_save

from apps.connection.models import ConnectionRequest, Connection


@receiver(post_save, sender=ConnectionRequest)
def create_connection(sender, instance, **kwargs):
    if instance.status == 1:
        Connection.objects.get_or_create(
            initiator=instance.sender, receiver=instance.recipient
        )
