import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from apps.user.models import UserProfile


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="password")


@pytest.fixture
def other_user(db):
    return User.objects.create_user(username="other", password="password")


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_profile_creating_signal(user):
    profile = UserProfile.objects.get(user=user)
    assert profile


def test_permission_denied_if_not_owner_PUT(client, other_user):
    client.login(username="testuser", password="password")
    url = reverse(f"profile-update-api", kwargs={"pk": other_user.id})
    data = {"bio": "Updated bio", "birth_date": "2000-01-01"}
    response = client.put(url, data, format="json")
    assert response.status_code == 403


def test_access_granted_GET(client, user):
    client.login(username="testuser", password="password")
    url = reverse(f"profile-retrieve-api", kwargs={"pk": user.id})
    response = client.get(url)

    assert response.status_code == 200
