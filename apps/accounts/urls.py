from django.urls import path
from .views import (
    SignUpView,
    LoginView,
    CustomLogoutView,
    ProfileDetailView,
    CustomUserUpdateView,
)
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("sign-up/", SignUpView.as_view(), name="sign-up"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path(
        "edit/",
        CustomUserUpdateView.as_view(),
        name="users-profile-edit",
    ),
    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/password_change.html"
        ),
        name="password_change",
    ),
    path(
        "password-change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path("<str:username>/", ProfileDetailView.as_view(), name="users-profile"),
    path("", ProfileDetailView.as_view(), name="user-profile"),
]
