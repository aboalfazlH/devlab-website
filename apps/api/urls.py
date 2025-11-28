from django.urls import path
from . import views


app_name = "api"
urlpatterns = [
    path(
        "front_json_placeholder/<int:count_article>/<int:count_user>",
        views.FrontFakeObjectsApi.as_view(),
    ),
    path("articles/<int:count_article>/", views.DevelopLabGetArticlesApi.as_view()),
]
