from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class SingUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    username = forms.CharField(
        max_length=254,
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        ),
    )


class UpdateProfileForm(forms.ModelForm):

    class Meta:
        from apps.user.models import UserProfile

        model = UserProfile
        fields = ["bio", "birth_date", "profile_picture"]
