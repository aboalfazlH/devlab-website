from django.urls import path
from . import views


urlpatterns = [
    path("question/",views.QuestionListView.as_view(),name="questions"),
    path("question/<slug:slug>/",views.QuestionDetailView.as_view(),name="question-detail")
]