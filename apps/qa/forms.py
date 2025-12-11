from django import forms
from .models import Question

class QuestionForm(forms.ModelForm):
    """Form definition for Question using Quill."""

    class Meta:
        model = Question
        fields = ("name", "help_image", "question_description", "slug", "categories")
        widgets = {
            "question_description": forms.Textarea(
                attrs={
                    "class": "quill-editor",
                    "style": "display:none;",
                }
            ),
            "categories": forms.SelectMultiple(attrs={"class": "form-select"}),  # اگر میخواید جایگزین Select2 شود
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ not in ["Textarea", "ClearableFileInput", "SelectMultiple"]:
                existing_classes = field.widget.attrs.get("class", "")
                field.widget.attrs["class"] = (existing_classes + " form-control").strip()
