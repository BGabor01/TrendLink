from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.post.serializers import (
    EditCreatePostSerializer,
    ListPostsSerializer,
    CreateCommentSerializer,
    CommentSerializer,
    UpdateCommentSerializer,
)
from apps.post.models import Post, Comment
from apps.post.permissions import IsOwnerOrPostOwnerOrReadOnly
from apps.user.permissions import IsOwnerOrReadOnly


class CreatePostView(generics.CreateAPIView):
    serializer_class = EditCreatePostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ListPostsView(generics.ListAPIView):
    serializer_class = ListPostsSerializer
    queryset = Post.objects.all().prefetch_related("comments")


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
