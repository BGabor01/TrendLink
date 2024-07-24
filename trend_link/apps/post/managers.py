from django.db.models.manager import Manager
from django.db.models import Subquery, Q, Exists, OuterRef


class PostManager(Manager):
    def only_connected_posts(self, request):
        from apps.post.models import Like
        from apps.connection.models import UserConnection

        connected_users_subquery = UserConnection.objects.filter(
            connections=request.user
        ).values('user')

        return (
            self.filter(
                Q(user__in=Subquery(connected_users_subquery)) | Q(
                    user=request.user))
                .select_related("user", "user__profile")
                .annotate(
                    has_liked=Exists(
                        Like.objects.filter(
                            user=request.user, post=OuterRef("pk"))
                    )
            )
            .order_by("-created_at"))
