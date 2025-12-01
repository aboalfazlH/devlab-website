from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser
from django.contrib.auth import authenticate


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
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "نام کاربری یا ایمیل"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "رمز عبور"})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("نام کاربری یا رمز عبور اشتباه است.")
        else:
            raise forms.ValidationError("تمامی فیلدها باید پر شوند.")

        return cleaned_data


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
