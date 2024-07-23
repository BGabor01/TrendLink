from django.db.models import Exists, Q
from django.contrib.auth.models import UserManager as BaseUserManager

from apps.connection.models import ConnectionRequest, UserConnection


class UserManager(BaseUserManager):
    """
    Custom manager for the User model.
    """

    def with_connection_info(self, user1, user2):
        """
        Annotate users with connection information between user1 and user2.
        Adds `pending` and `connected` annotations to indicate the connection status.
        """
        return self.select_related("profile").annotate(
            pending=Exists(
                ConnectionRequest.objects.filter(
                    Q(sender=user1, recipient=user2, status=0) |
                    Q(sender=user2, recipient=user1, status=0)
                )
            ),
            connected=Exists(
                UserConnection.objects.filter(
                    Q(user=user1, connections__connections=user2)
                )
            ),
        )
