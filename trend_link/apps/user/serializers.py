from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.user.models import UserProfile


class SignUpSerializer(serializers.ModelSerializer):
    """
    Serializer for user sign-up. Handles user creation and password validation.
    """
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def validate(self, data):
        """
        Validate that the two password fields match.
        """
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        """
        Create a new user with the validated data.
        """
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"]
        )
        user.set_password(validated_data["password1"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login. Authenticates the user based on provided credentials.
    """
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        """
        Validate the provided username and password.
        """
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User is deactivated.")
                data["user"] = user
            else:
                raise serializers.ValidationError(
                    "Unable to log in with provided credentials."
                )
        else:
            raise serializers.ValidationError(
                "Must include 'username' and 'password'."
            )

        return data


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile. Handles serialization of all profile fields.
    """
    class Meta:
        model = UserProfile
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the user model, including related profile and connection status.
    """
    profile = ProfileSerializer(read_only=True)
    pending = serializers.BooleanField(read_only=True)
    connected = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "profile",
            "connected",
            "pending",
        ]
