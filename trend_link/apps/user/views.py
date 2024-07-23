from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.user.serializers import (
    SignUpSerializer,
    LoginSerializer,
    ProfileSerializer,
    UserSerializer,
)
from apps.user.permissions import IsOwnerOrReadOnly
from apps.user.models import User, UserProfile


class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = authenticate(
            username=response.data.get("username"),
            password=request.data.get("password1")
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
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = UserProfile.objects.all().select_related("user")
    lookup_field = "pk"


class RetrieveProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "pk"

    def get_queryset(self):
        profile_user_id = self.kwargs["pk"]
        return User.objects.with_connection_info(self.request.user, profile_user_id)


class ListMembersView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            User.objects.exclude(id=self.request.user.id)
            .select_related("profile")
            .order_by("-date_joined")
        )
