from django import forms
from .models import Question
from django_summernote.widgets import SummernoteWidget


class QuestionForm(forms.ModelForm):
    """Form definition for Question."""

    class Meta:
        """Meta definition for QuestionForm."""

        model = Question
        fields = ("name","help_image","question_description","slug")
        widgets = {
            "question_description":SummernoteWidget()
        }        
