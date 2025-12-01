from django.urls import path
from . import views


urlpatterns = [
    path("questions",views.QuestionListView.as_view(),name="questions")
]