from django.urls import path
from . import views


app_name = "blog"

urlpatterns = [
    path("article/", views.ArticleListView.as_view(), name="articles"),
    path("article/write/", views.ArticleCreateView.as_view(), name="write-article"),
    path("article/<slug:slug>/", views.ArticleDetailView.as_view(), name="article-detail"),
    path("article/<slug:slug>/edit/", views.ArticleUpdateView.as_view(), name="article-update"),
    path("article/<slug:slug>/delete/", views.ArticleDeleteView.as_view(), name="article-delete"),
    path("article/<slug:slug>/pin/", views.ArticlePinView.as_view(), name="article-pin"),
    path("article/<slug:slug>/comment/write/", views.CommentCreateView.as_view(), name="comment-create"),
    path("article/<slug:slug>/comment/<int:comment_id>/delete/", views.CommentDeleteView.as_view(), name="comment-delete"),
    path("article/<slug:slug>/comment/<int:pk>/", views.CommentDetailView.as_view(), name="comment-detail"),
]
