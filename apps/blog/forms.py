from django import forms
from .models import Article


# Form for creating/updating articles
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "title",
            "slug",
            "thumbnail",
            "short_description",
            "description",
            "categories",
        ]
        widgets = {
            "description": forms.Textarea(
                attrs={"class": "summernote"}
            ),  # Summernote editor
            "categories": forms.SelectMultiple(
                attrs={"class": "django-select2"}
            ),  # Select2 for categories
        }
