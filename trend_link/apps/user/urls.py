from django.urls import path
from .views import SingUpView, LoginView, ProfileView, LogoutView

urlpatterns = [
    path("singup/", SingUpView.as_view(), name="singup"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
