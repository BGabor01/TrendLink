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
    path("api/singup/", SignUpView.as_view(), name="signup-api"),
    path(
        "signup/", TemplateView.as_view(template_name="user/signup.html"), name="signup"
    ),
    path("api/login/", LoginView.as_view(), name="login-api"),
    path("login/", TemplateView.as_view(template_name="user/login.html"), name="login"),
    path(
        "api/profile/<int:pk>/update/",
        UpdateProfileView.as_view(),
        name="profile-update-api",
    ),
    path(
        "api/profile/<int:pk>/",
        RetrieveProfileView.as_view(),
        name="profile-retrieve-api",
    ),
    path(
        "profile/<int:pk>/",
        TemplateView.as_view(template_name="user/profile.html"),
        name="profile",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("api/members/", ListMembersView.as_view(), name="members-api"),
    path(
        "members/",
        TemplateView.as_view(template_name="user/members.html"),
        name="members",
    ),
]
