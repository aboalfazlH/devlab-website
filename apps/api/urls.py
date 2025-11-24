from django.urls import path
from .views import FakeUsersView


app_name = "api"
urlpatterns = [
    path("fake_users/<int:count>/",FakeUsersView.as_view())   
]