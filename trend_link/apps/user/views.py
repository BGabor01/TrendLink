from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SingUpForm, LoginForm, UpdateProfileForm


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
        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
        return render(request, self.template_name, {"form": form})


class LogoutView(LoginRequiredMixin, View):

    def post(self, request):
        logout(request)
        return redirect("home")


class ProfileView(LoginRequiredMixin, View):
    form_class = UpdateProfileForm

    def get(self, request):
        from apps.user.models import UserProfile

        profile = get_object_or_404(UserProfile, user=request.user)
        return render(request, "user/profile.html", {"profile": profile})

    def post(self, request):
        from apps.user.models import UserProfile

        profile = get_object_or_404(UserProfile, user=request.user)
        form = self.form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
        return render(request, self.template_name, {"profile": profile, "form": form})


class HomeView(View):
    def get(self, request):
        return render(request, "user/home.html")
