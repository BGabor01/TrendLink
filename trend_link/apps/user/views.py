from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, UpdateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import url_has_allowed_host_and_scheme

from apps.user.forms import SingUpForm, LoginForm, UpdateProfileForm
from apps.user.permissions import IsUserProfileOwnerMixin


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
            next_url = request.GET.get("next")
            if next_url and url_has_allowed_host_and_scheme(
                next_url, allowed_hosts={request.get_host()}
            ):
                return redirect(next_url)
            return redirect("home")
        return render(request, self.template_name, {"form": form})


class LogoutView(LoginRequiredMixin, View):

    def post(self, request):
        logout(request)
        return redirect("login")


class ProfileView(LoginRequiredMixin, IsUserProfileOwnerMixin, UpdateView):
    from apps.user.models import UserProfile

    model = UserProfile
    form_class = UpdateProfileForm
    template_name = "user/profile.html"
    context_object_name = "profile"

    def get_success_url(self):
        return redirect("profile", pk=self.object.id).url

    def get_permission_denied_message(self) -> str:
        return "You have to be logged in to check a profile!"

    def get_login_url(self) -> str:
        return "login"


class ListMembersView(LoginRequiredMixin, ListView):
    template_name = "user/members.html"
    paginate_by = 10

    def get_queryset(self):
        from apps.user.models import UserProfile

        return UserProfile.objects.all().exclude(user=self.request.user)

    def get_success_url(self):
        return redirect("members").url

    def get_permission_denied_message(self) -> str:
        return "You have to be logged in to check a profile!"

    def get_login_url(self) -> str:
        return "login"
