from django.views.generic import TemplateView
from django.urls import path
from . import views


app_name = "api"
urlpatterns = [
    path(
        "json-placeholder/",
        views.FrontFakeObjectsApi.as_view(),
    ),
    path("articles/", views.DevelopLabGetArticlesApi.as_view()),
    path("articles/<str:token>/write-article", views.WriteArticle.as_view()),
    path("docs/", TemplateView.as_view(template_name="docs.html"), name="api-docs"),
]
