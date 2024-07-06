from django.urls import path
from .views import SingUpView, LoginView, ProfileView, LogoutView, ListMembersView

urlpatterns = [
    path("singup/", SingUpView.as_view(), name="singup"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/<int:id>", ProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("members/", ListMembersView.as_view(), name="members"),
]
