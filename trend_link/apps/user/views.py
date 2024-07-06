from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate

from .forms import SingUpForm, LoginForm


class SingUpView(View):
    form_class = SingUpForm
    template_name = "user/singup.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect("home")
        return render(request, self.template_name, {"form": form})


class LoginView(View):
    form_class = LoginForm
    template_name = "user/login.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
        return render(request, self.template_name, {"form": form})


class HomeView(View):
    def get(self, request):
        return render(request, "user/home.html")
