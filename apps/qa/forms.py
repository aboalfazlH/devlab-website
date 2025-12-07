from django import forms
from .models import Question
from django_summernote.widgets import SummernoteWidget
from django_select2.forms import Select2MultipleWidget

class QuestionForm(forms.ModelForm):
    """Form definition for Question."""

    class Meta:
        """Meta definition for QuestionForm."""

        model = Question
        fields = ("name","help_image","question_description","slug","categories")
        widgets = {
            "question_description":SummernoteWidget(),
            "categories":Select2MultipleWidget()
        }        
