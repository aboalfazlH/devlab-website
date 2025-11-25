from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    """Form definition for Article."""

    class Meta:
        """Meta definition for ArticleForm."""

        model = Article
        fields = ("title", "title","thumbnail","short_description","description",)
