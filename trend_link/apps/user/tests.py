import pytest
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpResponse
from django.test import RequestFactory
from django.core.exceptions import PermissionDenied

from apps.user.permissions import IsUserProfileOwnerMixin


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="password")


@pytest.mark.django_db
def test_profile_creating_signal(user):
    from apps.user.models import UserProfile

    profile = UserProfile.objects.get(user=user)

    assert profile


class TestView(IsUserProfileOwnerMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("User is owner!")

    def post(self, request, *args, **kwargs):
        return HttpResponse("User is owner!")


@pytest.fixture
def other_user(db):
    return User.objects.create_user(username="other", password="password")


@pytest.fixture
def factory():
    return RequestFactory()


def test_permission_denied_if_not_owner_POST(factory, other_user, user):
    from apps.user.models import UserProfile

    request = factory.get("/fake-url")
    request.user = other_user
    request.method = "POST"
    profile = UserProfile.objects.get(user=user)

    view = TestView.as_view()

    with pytest.raises(PermissionDenied):
        view(request, pk=profile.pk)


def test_access_granted_GET(factory, other_user, user):
    from apps.user.models import UserProfile

    request = factory.get("/fake-url")
    request.user = other_user
    request.method = "GET"
    profile = UserProfile.objects.get(user=user)

    view = TestView.as_view()

    response = view(request, pk=profile.pk)
    assert response.status_code == 200


def test_access_granted_POST(factory, user):
    from apps.user.models import UserProfile

    request = factory.get("/fake-url")
    request.user = user
    request.method = "POST"
    profile = UserProfile.objects.get(user=user)

    view = TestView.as_view()

    response = view(request, pk=profile.pk)

    assert response.status_code == 200
    assert response.content.decode() == "User is owner!"
