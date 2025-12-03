from django.urls import path
from . import views

app_name = "qa"

urlpatterns = [
    path("question/",views.QuestionListView.as_view(),name="questions"),
    path("question/ask/",views.QuestionCreateView.as_view(),name="question-create"),
    path("question/<slug:slug>/",views.QuestionDetailView.as_view(),name="question-detail"),
    path("question/<slug:slug>/edit/",views.QuestionUpdateView.as_view(),name="question-update"),
    path("question/<slug:slug>/delete/",views.QuestionDeleteView.as_view(),name="question-delete"),
]