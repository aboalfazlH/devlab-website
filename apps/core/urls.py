from django.urls import path
from . import views


app_name = "core"

urlpatterns = [
    path("", views.MainPageView.as_view(), name="home-page"),
    path("about-us/", views.AboutPageView.as_view(), name="about-us-page"),
    path("contact-us/", views.ContactPageView.as_view(), name="contact-us-page"),
    path("select2/categories/", views.CategoryAutocomplete.as_view(), name="categories-autocomplete"),
]
