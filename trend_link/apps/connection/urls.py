from django.urls import path
from django.views.generic import TemplateView

from apps.connection.views import (
    SendConnectionRequestView,
    ListConnectionRequests,
    AcceptConnectionRequestView,
    RejectConnectionRequestView,
)

urlpatterns = [
    # API Endpoints
    path("api/request/send/", SendConnectionRequestView.as_view(),
         name="api_send_connection_request"),
    path("api/request/list/", ListConnectionRequests.as_view(),
         name="api_list_connection_requests"),
    path("api/request/<int:pk>/accept/", AcceptConnectionRequestView.as_view(),
         name="api_accept_connection_request"),
    path("api/request/<int:pk>/reject/", RejectConnectionRequestView.as_view(),
         name="api_reject_connection_request"),

    # Template Views
    path("request/list/", TemplateView.as_view(template_name="connection/connection_reqs.html"),
         name="view_list_connection_requests"),
]
