from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView, DetailView, ListView

from myauth.forms import RegisterUserForm, ProfileUpdateForm
from myauth.models import Profile
from django.utils.translation import gettext_lazy as _, ngettext


class HelloView(View):
    wellcome_message = _("wellcome hello world")

    def get(self, request: HttpRequest) -> HttpResponse:
        items_str = request.GET.get("items") or 0
        items = int(items_str)
        products_line = ngettext(
            "one product",
            "{count} products",
            items,
        )
        products_line = products_line.format(count=items)
        return HttpResponse(
            f"<h1>{self.wellcome_message}</h1>"
            f"\n<h2>{products_line}</h2>")


class AboutMeView(TemplateView):
    template_name = 'myauth/about-me.html'
    model = Profile
    fields = "__all__"


class UsersListView(ListView):
    template_name = 'myauth/users-list.html'
    context_object_name = 'users'
    queryset = User.objects.all()


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('myauth:login')


class UserDetailsView(DetailView):
    template_name = 'myauth/user-details.html'
    model = User
    context_object_name = "user"


class AvatarUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        user = self.request.user
        profile = self.get_object()
        return user.is_staff or user.has_perm('myauth.change_profile') or user == profile.user

    model = Profile
    fields = "avatar",
    template_name_suffix = "_avatar_form"

    def get_success_url(self):
        return reverse_lazy(
            "myauth:user_details",
            kwargs={"pk": self.object.user.pk},
        )


class ProfileUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        user = self.request.user
        profile = self.get_object()
        return user == profile.user

    model = Profile
    fields = "bio", "agreement_accepted", "avatar",
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse_lazy(
            "myauth:user_details",
            kwargs={"pk": self.object.user.pk},
        )


class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    template_name = "myauth/register.html"  # Имя шаблона
    success_url = reverse_lazy('myauth:about-me')  # Переход на страницу с профайлом.

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request,
                            username=username,
                            password=password
                            )
        login(request=self.request, user=user)
        return response


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set!")


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value {value!r}")


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({'foo': 'bar', 'spam': 'eggs'})
