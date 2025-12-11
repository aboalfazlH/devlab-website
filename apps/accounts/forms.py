from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser
from django.contrib.auth import authenticate
from django.db.models import Q


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "نام کاربری"}),
            "email": forms.EmailInput(attrs={"placeholder": "ایمیل"}),
            "first_name": forms.TextInput(attrs={"placeholder": "نام"}),
            "last_name": forms.TextInput(attrs={"placeholder": "نام خانوادگی"}),
            "password1": forms.PasswordInput(),
            "password2": forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None
            field.label = ""
        self.fields["password1"].widget.attrs.update({"placeholder": "رمز عبور"})
        self.fields["password2"].widget.attrs.update({"placeholder": "تائید رمز عبور"})


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = "__all__"


class LoginForm(forms.Form):
    email = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "ایمیل"}),
        label="",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "رمز عبور"}),
        label="",
    )


class ProfileEditForm(forms.ModelForm):
    """Form definition for ProfileEdit."""

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "git_account",
            "avatar",
            "about",
            "bio",
            "public_email",
            "public_phone_number",
            "website",
            "facebook",
            "linkedin",
            "telegram",
            "public_article",
        )
        widgets = {
            "bio": forms.Textarea(
                attrs={
                    "class": "quill-editor",  # برای Quill
                    "style": "display:none;",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == "public_article":
                field.label = "عمومی بودن مقالات (نشان داده شدن در API)"
            else:
                field.label = ""
            if field.widget.__class__.__name__ not in ["CheckboxInput", "ClearableFileInput"]:
                existing_classes = field.widget.attrs.get("class", "")
                field.widget.attrs["class"] = (existing_classes + " form-control").strip()