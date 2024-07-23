import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from apps.connection.models import ConnectionRequest


@pytest.fixture
def sender(db):
    return User.objects.create_user(username="sender", password="password")


@pytest.fixture
def recipient(db):
    return User.objects.create_user(username="recipient", password="password")


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_create_connection_request(client, sender, recipient):
    client.login(username="sender", password="password")
    url = reverse("api_send_connection_request")
    data = {"recipient": recipient.id}

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert ConnectionRequest.objects.count() == 1
    assert ConnectionRequest.objects.get().sender == sender


@pytest.mark.django_db(transaction=True)
def test_create_duplicate_connection_request(client, sender, recipient):
    ConnectionRequest.objects.create(sender=sender, recipient=recipient)
    client.login(username="sender", password="password")

    url = reverse("api_send_connection_request")
    data = {"recipient": recipient.id}

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert ConnectionRequest.objects.count() == 1
    assert "detail" in response.data
    assert response.data["detail"] == "Connection request already exists."


@pytest.mark.django_db()
def test_create_duplicate_connection_request_reversed(client, sender, recipient):
    ConnectionRequest.objects.create(sender=sender, recipient=recipient)
    client.login(username="recipient", password="password")

    url = reverse("api_send_connection_request")
    data = {"recipient": sender.id}

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert ConnectionRequest.objects.count() == 1
