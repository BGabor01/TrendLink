from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


class UserIsOwner:
    model = None
    user_field = "user"

    def dispatch(self, request, *args, **kwargs):
        if not self.model:
            raise ValueError("Model attribute must be set")

        obj = get_object_or_404(self.model, pk=kwargs["pk"])
        if (
            request.method not in ["GET", "HEAD", "OPTIONS", "TRACE"]
            and getattr(obj, self.user_field) != request.user
        ):
            raise PermissionDenied

        kwargs["obj"] = obj
        return super().dispatch(request, *args, **kwargs)


class IsUserProfileOwnerMixin(UserIsOwner):
    from apps.user.models import UserProfile

    model = UserProfile
