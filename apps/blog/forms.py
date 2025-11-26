from django import forms
from .models import Article
from django_summernote.widgets import SummernoteWidget

class ArticleForm(forms.ModelForm):
    """Form definition for Article."""

    class Meta:
        """Meta definition for ArticleForm."""

        model = Article
        fields = ("title", "slug","thumbnail","short_description","description",)
        widgets = {
            "description": SummernoteWidget(),
        }