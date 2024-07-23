from django.urls import path
from .views import (
    LoginView,
    UpdateProfileView,
    RetrieveProfileView,
    LogoutView,
    ListMembersView,
    SignUpView,
)
from django.views.generic import TemplateView

urlpatterns = [
    # API Endpoints
    path("api/signup/", SignUpView.as_view(), name="api_signup"),
    path("api/login/", LoginView.as_view(), name="api_login"),
    path("api/profile/<int:pk>/update/",
         UpdateProfileView.as_view(), name="api_profile_update"),
    path("api/profile/<int:pk>/", RetrieveProfileView.as_view(),
         name="api_profile_detail"),
    path("api/members/", ListMembersView.as_view(), name="api_members_list"),

    # Template Views
    path("signup/", TemplateView.as_view(template_name="user/signup.html"),
         name="view_signup"),
    path("login/", TemplateView.as_view(template_name="user/login.html"),
         name="view_login"),
    path("profile/<int:pk>/",
         TemplateView.as_view(template_name="user/profile.html"), name="view_profile"),
    path("members/", TemplateView.as_view(template_name="user/members.html"),
         name="view_members"),
    path("logout/", LogoutView.as_view(), name="view_logout"),
]
