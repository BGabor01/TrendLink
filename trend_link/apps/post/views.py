from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.db.models import Exists, OuterRef
from django.db import IntegrityError

from apps.post.serializers import (
    EditCreatePostSerializer,
    ListPostsSerializer,
    CreateCommentSerializer,
    CommentSerializer,
    UpdateCommentSerializer,
    LikePostSerializer,
    PostSerializer,
)
from apps.post.models import Post, Comment, Like
from apps.post.permissions import IsOwnerOrPostOwnerOrReadOnly
from apps.user.permissions import IsOwnerOrReadOnly
from apps.post.paginations import PostCursorPagination


class CreatePostView(generics.CreateAPIView):
    serializer_class = EditCreatePostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ListPostsView(generics.ListAPIView):
    serializer_class = ListPostsSerializer
    pagination_class = PostCursorPagination

    def get_queryset(self):
        return (
            Post.objects.all()
            .prefetch_related("comments", "comments__user", "comments__user__profile")
            .select_related("user", "user__profile")
            .annotate(
                has_liked=Exists(
                    Like.objects.filter(
                        user=self.request.user, post=OuterRef("pk"))
                )
            )
            .order_by("-created_at")
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "request": self.request,
            }
        )
        return context


class UpdatePostView(generics.UpdateAPIView):
    serializer_class = EditCreatePostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    lookup_field = "pk"


class DeletePostView(generics.DestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    lookup_field = "pk"


class CreateCommentView(generics.CreateAPIView):
    serializer_class = CreateCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class DeleteCommentView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrPostOwnerOrReadOnly]
    queryset = Comment.objects.all()
    lookup_field = "pk"


class UpdateCommentView(generics.UpdateAPIView):
    serializer_class = UpdateCommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Comment.objects.all()
    lookup_field = "pk"


class LikePostView(generics.CreateAPIView):
    serializer_class = LikePostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            return serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError(
                {"detail": "User already liked this post"}, status.HTTP_400_BAD_REQUEST
            )


class UnlikePostView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        post_id = self.kwargs["post_id"]
        user = self.request.user
        try:
            like = Like.objects.get(post_id=post_id, user=user)
            return like
        except Like.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        like = self.get_object()
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
