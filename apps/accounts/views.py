from .forms import CustomUserCreationForm, LoginForm, ProfileEditForm
from django.views.generic import CreateView, FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, ProfileLink
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.blog.models import Article
from django.db.models import Q
from django.shortcuts import get_object_or_404

class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("core:home-page")
    template_name = "accounts/auth/sign-up.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class LoginView(FormView):
    form_class = LoginForm
    template_name = "accounts/auth/login.html"
    success_url = reverse_lazy("core:home-page")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user_username = get_object_or_404(CustomUser, Q(username=username) | Q(email=username)).username
        user = authenticate(self.request, username=user_username, password=password)
                
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"خوش آمدید {self.request.user}")
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
        return render(request, "accounts/auth/logout-confirm.html")

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "با موفقیت خارج شدید")
        return redirect(self.success_url)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "accounts/profile.html"
    context_object_name = "profile"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_object(self, queryset=None):
        username = self.kwargs.get(self.slug_url_kwarg)

        if username:
            return get_object_or_404(CustomUser, username__iexact=username)

        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context["profile"]

        context["articles"] = Article.objects.filter(
            author=user, is_active=True
        ).order_by("-write_date", "-views")[:10]

        context["links"] = ProfileLink.objects.filter(user=user)

        return context


class CustomUserUpdateView(UpdateView):
    model = CustomUser
    template_name = "accounts/user_update_profile.html"
    form_class = ProfileEditForm
    success_url = reverse_lazy("user-profile")

    def get_object(self, queryset=None):
        return self.request.user
