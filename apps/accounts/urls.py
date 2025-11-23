from django.urls import path
from .views import SignUpView,LoginView,CustomLogoutView


urlpatterns = [
    path('sign-up/',SignUpView.as_view(),name="sign-up"),
    path('login/',LoginView.as_view(),name="login"),
    path('logout/',CustomLogoutView.as_view(),name="logout"),
]