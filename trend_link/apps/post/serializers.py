from rest_framework import serializers
from django.shortcuts import get_object_or_404

from apps.post.models import Post, Comment
from apps.user.serializers import UserSerializer, ProfileSerializer


class EditCreatePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["text", "image"]

    def validate(self, data):
        text = data.get("text")
        image = data.get("image")

        if not text and not image:
            raise serializers.ValidationError(
                "At least one of Text or Image must be provided.", 400
            )

        return data


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


class ListPostsSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"


class CreateCommentSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = ["post_id", "text"]

    def validate_post_id(self, value):
        get_object_or_404(Post, id=value)
        return value

    def create(self, validated_data):
        post_id = validated_data.pop("post_id")
        post = get_object_or_404(Post, id=post_id)
        comment = Comment.objects.create(post=post, **validated_data)
        return comment

    def to_representation(self, instance):
        return CommentSerializer(instance).data


class UpdateCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ["text"]
