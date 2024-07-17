from rest_framework import serializers
from apps.post.models import Post, Comment, Like
from apps.user.serializers import UserSerializer
from apps.post.paginations import CommentPagination


class EditCreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["text", "image", "tags"]

    def validate(self, data):
        text = data.get("text")
        image = data.get("image")
        if not text and not image:
            raise serializers.ValidationError(
                "At least one of Text or Image must be provided.", 400
            )
        return data


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


class ListPostsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_has_liked(self, obj):
        return obj.has_liked

    def get_comments(self, obj):
        comments = obj.comments.all()
        paginator = CommentPagination()
        page = paginator.paginate_queryset(comments, self.context["request"])
        serializer = CommentSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data).data


class CreateCommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ["post", "text"]

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def to_representation(self, instance):
        return CommentSerializer(instance).data


class UpdateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["text"]


class LikePostSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Like
        fields = ["post"]
