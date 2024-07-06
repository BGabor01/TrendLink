from django.urls import path
from .views import SingUpView, HomeView

urlpatterns = [
    path("singup/", SingUpView.as_view(), name="singup"),
]
