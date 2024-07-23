from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrPostOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object or the owner of the associated post to edit it.
    Read-only access is allowed for non-owners.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user or obj.post.user == request.user
