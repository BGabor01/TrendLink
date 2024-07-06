from django.urls import path
from .views import SingUpView, LoginView

urlpatterns = [
    path("singup/", SingUpView.as_view(), name="singup"),
    path("login/", LoginView.as_view(), name="login"),
]
