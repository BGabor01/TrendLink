from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Exists, OuterRef

from apps.post.serializers import (
    EditCreatePostSerializer,
    ListPostsSerializer,
    CreateCommentSerializer,
    CommentSerializer,
    UpdateCommentSerializer,
    CreateLikeSerializer,
    PostSerializer,
)
from apps.post.models import Post, Comment, Like
from apps.post.permissions import IsOwnerOrPostOwnerOrReadOnly
from apps.user.permissions import IsOwnerOrReadOnly


class CreatePostView(generics.CreateAPIView):
    serializer_class = EditCreatePostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ListPostsView(generics.ListAPIView):
    serializer_class = ListPostsSerializer

    def get_queryset(self):
        return (
            Post.objects.all()
            .prefetch_related("comments")
            .select_related("user")
            .annotate(
                has_liked=Exists(
                    Like.objects.filter(user=self.request.user, post=OuterRef("pk"))
                )
            )
        )


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


class CreateLikeView(generics.CreateAPIView):
    serializer_class = CreateLikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
