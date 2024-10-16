from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.post.models import Post, Comment, Like
from apps.post.paginations import PostCursorPagination
from apps.post.permissions import IsOwnerOrPostOwnerOrReadOnly
from apps.post.serializers import (
    EditCreatePostSerializer,
    ListPostsSerializer,
    CreateCommentSerializer,
    CommentSerializer,
    UpdateCommentSerializer,
    LikePostSerializer,
    PostSerializer,
)
from apps.user.permissions import IsOwnerOrReadOnly


class CreatePostView(generics.CreateAPIView):
    serializer_class = EditCreatePostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ListPostsView(generics.ListAPIView):
    serializer_class = ListPostsSerializer
    pagination_class = PostCursorPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.only_connected_posts(self.request)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
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
            return Like.objects.get(post_id=post_id, user=user)
        except Like.DoesNotExist:
            raise ValidationError(
                {"detail": "Like not found"}, status.HTTP_404_NOT_FOUND
            )

    def delete(self, *args, **kwargs):
        like = self.get_object()
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
