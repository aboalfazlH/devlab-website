from django.urls import path
from . import views


app_name = "api"
urlpatterns = [
    path(
        "front_json_placeholder/",
        views.FrontFakeObjectsApi.as_view(),
    ),
    path("articles/", views.DevelopLabGetArticlesApi.as_view()),
    path("articles/<str:token>/write-article", views.WriteArticle.as_view()),
]
