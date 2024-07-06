import pytest
from django.contrib.auth.models import User


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="password")


@pytest.mark.django_db
def test_profile_creating_signal(user):
    from apps.user.models import UserProfile

    profile = UserProfile.objects.get(user=user)

    assert profile
