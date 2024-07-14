from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserConnection(models.Model):
    initiator = models.ForeignKey(
        User,
        related_name="initiated",
        on_delete=models.CASCADE,
    )
    receiver = models.ForeignKey(
        User,
        related_name="receiver",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        app_label = "connection"
        unique_together = ("initiator", "receiver")
        indexes = [
            models.Index(fields=["initiator", "receiver"]),
        ]

    def __str__(self):
        return f"Connection({self.initiator} and {self.receiver})"


class ConnectionRequest(models.Model):
    STATUS_CHOICES = (
        (0, "Pending"),
        (1, "Accepted"),
        (2, "Rejected"),
    )
    sender = models.ForeignKey(
        User,
        related_name="sender",
        related_query_name="sender",
        on_delete=models.CASCADE,
    )
    recipient = models.ForeignKey(
        User,
        related_name="recipient",
        related_query_name="recipient",
        on_delete=models.CASCADE,
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        app_label = "connection"
        indexes = [
            models.Index(fields=["sender", "recipient"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["sender", "recipient"], name="unique_sender_recipient_pair"
            ),
        ]

    def __str__(self):
        return f"ConnectionRequest(from {self.sender} to {self.recipient})"

    def accept(self):
        self.status = 1
        self.save()

    def reject(self):
        self.status = 2
        self.save()


User.add_to_class(
    "connections",
    models.ManyToManyField(
        "self",
        through=UserConnection,
        symmetrical=True,
    ),
)
