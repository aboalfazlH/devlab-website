from django.urls import path
from .views import MainPageView, AboutPageView, ContactPageView


app_name = "core"

urlpatterns = [
    path("", MainPageView.as_view(), name="home-page"),
    path("about-us/", AboutPageView.as_view(), name="about-us-page"),
    path("contact-us/", ContactPageView.as_view(), name="contact-us-page"),
]
