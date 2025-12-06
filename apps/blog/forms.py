from django import forms
from .models import Article
from django_summernote.widgets import SummernoteWidget

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
            "title":forms.TextInput(
                attrs={"class":"article-title","placeholder":"موضوع"}
            ),
            "slug":forms.TextInput(
                attrs={"class":"article-slug","placeholder":"شناسه"}
            ),
            "short_description":forms.TextInput(
                attrs={"class":"article-short-description","placeholder":"خلاصه"}
            ),
            "description": forms.Textarea(
                attrs={"class": "summernote"}
            ),
            "categories": forms.SelectMultiple(
                attrs={"class": "django-select2"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.label = ""

        for field in self.fields.values():
            field.help_text = ""
