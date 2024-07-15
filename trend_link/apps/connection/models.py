from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class UserConnection(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="connections",
        related_query_name="connections",
    )
    connections = models.ManyToManyField(User, blank=True, symmetrical=True)

    def __str__(self) -> str:
        return f"{self.user.username}'s connection list"


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
