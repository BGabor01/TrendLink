from django.shortcuts import redirect
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import login, authenticate, logout

from apps.user.serializers import (
    SignUpSerializer,
    LoginSerializer,
    ProfileSerializer,
)
from apps.user.permissions import IsOwner


class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = authenticate(
            username=response.data["username"], password=request.data["password1"]
        )
        if user:
            login(request, user)
        return response


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return Response({"detail": "Login successful."}, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):

    def post(self, request):
        logout(request)
        return redirect("login")


class UpdateProfileView(generics.UpdateAPIView):
    from apps.user.models import UserProfile

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = UserProfile.objects.all().select_related("user")
    lookup_field = "pk"


class RetrieveProfileView(generics.RetrieveAPIView):
    from apps.user.models import UserProfile

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all().select_related("user")
    lookup_field = "pk"


class ListMembersView(generics.ListAPIView):

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from apps.user.models import UserProfile

        return UserProfile.objects.exclude(user=self.request.user).select_related(
            "user"
        )
