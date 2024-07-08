from rest_framework import serializers
from apps.post.models import Post


class EditCreatePostSerializer(serializers.ModelSerializer):

    def validate(self, data):
        text = data.get("text")
        image = data.get("image")

        if not text and not image:
            raise serializers.ValidationError(
                "At least one of Text or Image must be provided.", 400
            )

        return data

    class Meta:
        model = Post
        fields = ["text", "image"]
