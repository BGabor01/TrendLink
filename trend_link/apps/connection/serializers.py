from rest_framework import serializers
from django.contrib.auth.models import User

from apps.connection.models import ConnectionRequest


class SendConnectionRequestSerializer(serializers.ModelSerializer):
    recipient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ConnectionRequest
        fields = ["recipient"]
