from rest_framework import serializers
from django.contrib.auth.models import User

from apps.connection.models import ConnectionRequest
from apps.user.serializers import UserSerializer


class SendConnectionRequestSerializer(serializers.ModelSerializer):
    recipient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ConnectionRequest
        fields = ["recipient"]

    def validate(self, data):
        sender = self.context["request"].user
        recipient = data.get("recipient")

        if ConnectionRequest.objects.filter(
            sender=recipient, recipient=sender
        ).exists():
            raise serializers.ValidationError(
                "A reverse connection request already exists.", 400
            )

        return data


class ConnectionRequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = ConnectionRequest
        fields = "__all__"


class ConnectionRequestActionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConnectionRequest
        fields = []
