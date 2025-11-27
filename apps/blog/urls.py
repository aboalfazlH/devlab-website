from django.urls import path
from .views import (
    ArticleListView,
    ArticleCreateView,
    ArticleDetailView,
    ArticleUpdateView,
    ArticleDeleteView,
    ArticlePinView,
    CategoryAutocomplete,
)

app_name = "blog"

urlpatterns = [
    path("article/", ArticleListView.as_view(), name="articles"),
    path("article/write/", ArticleCreateView.as_view(), name="write-article"),
    path("article/<slug:slug>/", ArticleDetailView.as_view(), name="article-detail"),
    path(
        "article/<slug:slug>/edit/", ArticleUpdateView.as_view(), name="article-update"
    ),
    path(
        "article/<slug:slug>/delete/",
        ArticleDeleteView.as_view(),
        name="article-delete",
    ),
    path("article/<slug:slug>/pin/", ArticlePinView.as_view(), name="article-pin"),
    path(
        "select2/categories/",
        CategoryAutocomplete.as_view(),
        name="categories-autocomplete",
    ),
]
