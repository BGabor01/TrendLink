from django.urls import path

from apps.connection.views import SendConnectionRequestView

urlpatterns = [
    path("api/send", SendConnectionRequestView.as_view(), name="send-connectionreq-api")
]
