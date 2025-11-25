from django.urls import path
from .views import ArticleListView,ArticleCreateView,ArticleDetailView

app_name = "blog"

urlpatterns = [
    path("article/", ArticleListView.as_view(), name="articles"),
    path("article/write/",ArticleCreateView.as_view(),name="write_article"),
    path("article/<slug:slug>",ArticleDetailView.as_view(),name="article-detail"),
]
