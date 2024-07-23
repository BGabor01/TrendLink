from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.connection.models import ConnectionRequest
from apps.connection.serializers import (
    SendConnectionRequestSerializer,
    ConnectionRequestSerializer,
    ConnectionRequestActionsSerializer,
)


class SendConnectionRequestView(generics.CreateAPIView):
    serializer_class = SendConnectionRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save(sender=self.request.user)
        except IntegrityError:
            raise ValidationError(
                {"detail": "Connection request already exists."},
                code=status.HTTP_400_BAD_REQUEST,
            )


class ListConnectionRequests(generics.ListAPIView):
    serializer_class = ConnectionRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            ConnectionRequest.objects.filter(
                recipient=self.request.user, status=0)
            .select_related("sender")
            .order_by("-created_at")
        )


class AcceptConnectionRequestView(generics.UpdateAPIView):
    serializer_class = ConnectionRequestActionsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        return ConnectionRequest.objects.filter(recipient=self.request.user, status=0)

    def update(self):
        instance = self.get_object()
        instance.accept()
        return Response({"status": "accepted"}, status=status.HTTP_200_OK)


class RejectConnectionRequestView(generics.DestroyAPIView):
    serializer_class = ConnectionRequestActionsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        return ConnectionRequest.objects.filter(recipient=self.request.user, status=0)

    def destroy(self):
        instance = self.get_object()
        instance.reject()
        return Response(status=status.HTTP_204_NO_CONTENT)
