from django.contrib.auth.models import UserManager
from django.db import models
from django.db.models import Q, Exists
from apps.connection.models import ConnectionRequest
from apps.connection.models import UserConnection


class UserManager(UserManager):
    def with_connection_info(self, user1, user2):
        return self.select_related("profile").annotate(
            pending=Exists(
                ConnectionRequest.objects.filter(
                    Q(sender=user1, recipient=user2, status=0)
                    | Q(sender=user2, recipient=user1, status=0)
                )
            ),
            connected=Exists(
                UserConnection.objects.filter(
                    Q(user=user1, connections__connections=user2)
                )
            ),
        )
