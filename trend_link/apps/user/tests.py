import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory
from rest_framework.test import force_authenticate
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated

from apps.user.permissions import IsOwnerOrReadOnly
from apps.user.serializers import ProfileSerializer
from apps.user.models import UserProfile


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="password")


@pytest.mark.django_db
def test_profile_creating_signal(user):
    from apps.user.models import UserProfile

    profile = UserProfile.objects.get(user=user)
    assert profile


class TestView(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView
):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = UserProfile.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


@pytest.fixture
def other_user(db):
    return User.objects.create_user(username="other", password="password")


@pytest.fixture
def factory():
    return RequestFactory()


def test_permission_denied_if_not_owner_PUT(factory, other_user, user):
    from apps.user.models import UserProfile

    data = {"bio": "Updated bio", "birth_date": "2000-01-01"}
    request = factory.put("/fake-url", data, content_type="application/json")
    request.user = other_user
    profile = UserProfile.objects.get(user=user)

    view = TestView.as_view()
    force_authenticate(request, user=other_user)
    response = view(request, pk=profile.pk)
    assert response.status_code == 403


def test_access_granted_GET(factory, user):
    from apps.user.models import UserProfile

    request = factory.get("/fake-url")
    request.user = user
    profile = UserProfile.objects.get(user=user)

    view = TestView.as_view()
    force_authenticate(request, user=user)
    response = view(request, pk=profile.pk)
    assert response.status_code == 200


