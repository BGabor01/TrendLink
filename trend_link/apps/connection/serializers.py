from rest_framework import serializers
from django.contrib.auth.models import User

from apps.connection.models import ConnectionRequest
from apps.user.serializers import UserSerializer


class SendConnectionRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for sending a connection request.
    """
    recipient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ConnectionRequest
        fields = ["recipient"]

    def validate(self, data):
        """
        Validate that there is no reverse connection request already existing.
        """
        sender = self.context["request"].user
        recipient = data.get("recipient")

        if ConnectionRequest.objects.filter(sender=recipient, recipient=sender).exists():
            raise serializers.ValidationError(
                "A reverse connection request already exists.", 400
            )

        return data


class ConnectionRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for connection request details, including the sender information.
    """
    sender = UserSerializer(read_only=True)

    class Meta:
        model = ConnectionRequest
        fields = "__all__"


class ConnectionRequestActionsSerializer(serializers.ModelSerializer):
    """
    Serializer for connection request actions (accept/reject).
    """
    class Meta:
        model = ConnectionRequest
        fields = []
