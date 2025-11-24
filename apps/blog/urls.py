from django.urls import path
from .views import ArticleListView

app_name = "blog"

urlpatterns = [
    path("articles/", ArticleListView.as_view(), name="articles"),
]
