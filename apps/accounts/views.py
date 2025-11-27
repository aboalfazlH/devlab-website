from .forms import CustomUserCreationForm, LoginForm, ProfileEditForm
from django.views.generic import CreateView, FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("admin:index")
    template_name = "sign-up.html"


class LoginView(FormView):
    form_class = LoginForm
    template_name = "login.html"
    success_url = reverse_lazy("core:home-page")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            messages.success(self.request, f"خوش آمدید {self.request.user}")
            login(self.request, user)
            return super().form_valid(form)

        form.add_error(None, "نام کاربری یا رمز عبور اشتباه است.")
        return self.form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "شما اکنون احراز هویت کردید")
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)


class CustomLogoutView(LoginRequiredMixin, FormView):
    success_url = reverse_lazy("core:home-page")

    def get(self, request, *args, **kwargs):
        return render(request, "logout-confirm.html")

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "با موفقیت خارج شدید")
        return redirect(self.success_url)


class CustomUserDetailView(DetailView):
    model = CustomUser
    template_name = "profile.html"
    context_object_name = "profile"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_object(self, queryset=None):
        username = self.kwargs.get(self.slug_url_kwarg)
        return get_object_or_404(CustomUser, username__iexact=username)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "profile.html"
    context_object_name = "profile"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_object(self, queryset=None):
        return self.request.user


class CustomUserUpdateView(UpdateView):
    model = CustomUser
    template_name = "user_update_profile.html"
    form_class = ProfileEditForm
    success_url = reverse_lazy("user-profile")

    def get_object(self, queryset=None):
        return self.request.user
