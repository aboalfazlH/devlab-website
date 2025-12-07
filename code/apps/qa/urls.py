from django.urls import path
from . import views

app_name = "qa"

urlpatterns = [
    path("question/",views.QuestionListView.as_view(),name="questions"),
    path("question/ask/",views.QuestionCreateView.as_view(),name="question-create"),
    path("question/<slug:slug>/",views.QuestionDetailView.as_view(),name="question-detail"),
    path("question/<slug:slug>/edit/",views.QuestionUpdateView.as_view(),name="question-update"),
    path("question/<slug:slug>/delete/",views.QuestionDeleteView.as_view(),name="question-delete"),
    path("question/<slug:slug>/like/",views.QuestionLikeView.as_view(),name="like-question"),
    path("question/<slug:slug>/dislike/",views.QuestionDisLikeView.as_view(),name="dislike-question"),
    path("question/<slug:slug>/answer/new",views.AnswerCreateView.as_view(),name="answer-create"),
    path("question/<slug:slug>/answer/<int:pk>/edit/",views.AnswerUpdateView.as_view(),name="answer-edit"),
    path("question/<slug:slug>/answer/<int:pk>/delete/",views.AnswerDeleteView.as_view(),name="answer-delete"),
    path("question/<slug:slug>/answer/<int:pk>/best/",views.AnswerBestView.as_view(),name="answer-best"),
    path("question/<slug:slug>/answer/<int:pk>/like/",views.AnswerLikeView.as_view(),name="answer-like"),
    path("question/<slug:slug>/answer/<int:pk>/dislike/",views.AnswerDisLikeView.as_view(),name="answer-dislike"),
]
