from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django_summernote.admin import SummernoteModelAdmin
from .models import CustomUser,ProfileLink
from .forms import CustomUserChangeForm, CustomUserCreationForm


@admin.register(CustomUser)
class CustomUserAdmin(SummernoteModelAdmin,UserAdmin):
    """Admin View for CustomUser"""
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = (
        "username",
        "get_full_name",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_display_links = ("username",)
    list_editable = ("is_active", "is_staff", "is_superuser")
    list_filter = ("is_active", "is_staff", "is_superuser", "date_joined", "last_login")
    readonly_fields = ("date_joined", "last_login")
    search_fields = ("username", "get_full_name")
    date_hierarchy = "date_joined"
    ordering = (
        "-last_login",
        "-date_joined",
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "phone_number", "email", "password"),
            },
        ),
        (
            "personal_info",
            {
                "classes": ("wide",),
                "fields": ("first_name", "last_name", "about", "bio", "avatar","git_account"),
            },
        ),
        (
            "date&times",
            {
                "classes": ("collapse",),
                "fields": ("date_joined", "last_login"),
            },
        ),
        (
            "advanced",
            {
                "classes": ("collapse",),
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

admin.site.register(ProfileLink,)