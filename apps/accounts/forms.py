from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser


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
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "نام کاربری یا ایمیل"})
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "رمز"}))


class ProfileEditForm(forms.ModelForm):
    """Form definition for ProfileEdit."""

    class Meta:
        """Meta definition for ProfileEditForm."""

        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "git_account",
            "avatar",
            "about",
            "bio",
            "email",
            "public_email",
            "public_phone_number",
            "phone_number",
            "git_account",
            "website",
            "facebook",
            "linkedin",
            "telegram",
            "public_article",
        )
