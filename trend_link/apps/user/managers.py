from django.contrib.auth.models import UserManager
from django.db import models
from django.db.models import Case, When, Q, Value, BooleanField, Exists
from apps.connection.models import ConnectionRequest


class UserManager(UserManager):
    def with_connection_info(self, user1, user2):
        return (
            self.select_related("profile")
            .prefetch_related("connections")
            .annotate(
                connected=Case(
                    When(
                        Q(connections__id=user2),
                        then=Value(True),
                    ),
                    default=Value(False),
                    output_field=BooleanField(),
                ),
                pending=Exists(
                    ConnectionRequest.objects.filter(
                        Q(sender=user1, recipient=user2, status=0)
                        | Q(sender=user2, recipient=user1, status=0)
                    )
                ),
            )
        )
