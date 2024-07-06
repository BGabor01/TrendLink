from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SingUpForm, LoginForm, UpdateProfileForm


class SingUpView(View):
    form_class = SingUpForm
    template_name = "user/singup.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
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

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
        return render(request, self.template_name, {"form": form})


class LogoutView(LoginRequiredMixin, View):

    def post(self, request):
        logout(request)
        return redirect("login")


class ProfileView(LoginRequiredMixin, View):
    form_class = UpdateProfileForm
    template_name = "user/profile.html"

    def get(self, request, id):
        from apps.user.models import UserProfile

        profile = get_object_or_404(UserProfile, user=id)
        form = UpdateProfileForm(instance=request.user.profile)
        return render(request, "user/profile.html", {"profile": profile, "form": form})

    def post(self, request, id):
        from apps.user.models import UserProfile

        profile = get_object_or_404(UserProfile, user=id)
        form = self.form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile", id=id)
        return render(request, self.template_name, {"profile": profile, "form": form})


class ListMembersView(LoginRequiredMixin, ListView):
    template_name = "user/members.html"
    paginate_by = 10

    def get_queryset(self):
        from apps.user.models import UserProfile

        return UserProfile.objects.all().exclude(user=self.request.user)


class HomeView(View):
    def get(self, request):
        return render(request, "user/home.html")
