from django.urls import path
from django.views.generic import TemplateView

from apps.connection.views import (
    SendConnectionRequestView,
    ListConnectionRequests,
    AcceptConnectionRequestView,
    RejectConnectionRequestView,
)

urlpatterns = [
    path(
        "api/request/send/",
        SendConnectionRequestView.as_view(),
        name="send-connectionreq-api",
    ),
    path(
        "request/list/",
        TemplateView.as_view(template_name="connection/connection_reqs.html"),
        name="list-connectionreq",
    ),
    path(
        "api/request/list/",
        ListConnectionRequests.as_view(),
        name="list-connectionreq-api",
    ),
    path(
        "api/request/<int:pk>/accept/",
        AcceptConnectionRequestView.as_view(),
        name="accept-connectionreq-api",
    ),
    path(
        "api/request/<int:pk>/reject/",
        RejectConnectionRequestView.as_view(),
        name="reject-connectionreq-api",
    ),
]
