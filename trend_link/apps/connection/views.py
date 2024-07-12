from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.connection.serializers import SendConnectionRequestSerializer


class SendConnectionRequestView(generics.CreateAPIView):
    serializer_class = SendConnectionRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(sender=self.request.user)
