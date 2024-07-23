from rest_framework import serializers

from apps.post.models import Post, Comment, Like
from apps.user.serializers import UserSerializer
from apps.post.paginations import CommentPagination


class EditCreatePostSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and editing a post.
    """
    class Meta:
        model = Post
        fields = ["text", "image", "tags"]

    def validate(self, data):
        """
        Validate that at least one of text or image is provided.
        """
        text = data.get("text")
        image = data.get("image")
        if not text and not image:
            raise serializers.ValidationError(
                "At least one of Text or Image must be provided.", 400
            )
        return data


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model, including all fields.
    """
    class Meta:
        model = Post
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model, including the related user.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


class ListPostsSerializer(serializers.ModelSerializer):
    """
    Serializer for listing posts, including related user, comments, and like status.
    """
    user = UserSerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_has_liked(self, obj):
        """
        Return whether the current user has liked the post.
        """
        return obj.has_liked

    def get_comments(self, obj):
        """
        Paginate and serialize the comments for the post.
        """
        comments = obj.comments.all()
        paginator = CommentPagination()
        page = paginator.paginate_queryset(comments, self.context["request"])
        serializer = CommentSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data).data


class CreateCommentSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a comment, linked to a specific post.
    """
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ["post", "text"]

    def create(self, validated_data):
        """
        Create and return a new comment instance.
        """
        return Comment.objects.create(**validated_data)

    def to_representation(self, instance):
        """
        Serialize the comment instance.
        """
        return CommentSerializer(instance).data


class UpdateCommentSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a comment, allowing changes to the text.
    """
    class Meta:
        model = Comment
        fields = ["text"]


class LikePostSerializer(serializers.ModelSerializer):
    """
    Serializer for liking a post, linked to a specific post.
    """
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Like
        fields = ["post"]
