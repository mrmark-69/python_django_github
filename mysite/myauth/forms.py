from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from myauth.models import Profile


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Login", widget=forms.TextInput())
    email = forms.EmailField(label="Email", widget=forms.EmailInput())
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
