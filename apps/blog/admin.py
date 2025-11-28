from django.contrib import admin
from .models import Article, ArticleCategory
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = "description"
    """Admin View for Article"""
    list_display = (
        "title",
        "is_active",
        "is_verify",
        "is_pin",
        "status",
        "write_date",
        "update_date",
        "delete_date",
        "verify_date",
    )
    list_editable = ("is_active", "is_pin", "is_verify")
    list_filter = (
        "is_active",
        "is_verify",
        "is_pin",
        "write_date",
        "update_date",
        "delete_date",
        "verify_date",
    )
    autocomplete_fields = ("author","categories",)
    readonly_fields = (
        "write_date",
        "update_date",
        "delete_date",
        "verify_date",
    )
    search_fields = (
        "title",
        "description",
        "short_description",
    )
    date_hierarchy = "write_date"
    ordering = ("-write_date", "is_active")
    list_per_page = 20
    fieldsets = (
        (
            "اطلاعات اصلی",
            {
                "classes": ("wide",),
                "fields": (
                    "title",
                    "short_description",
                    "description",
                    "thumbnail",
                    "slug",
                    "author",
                ),
            },
        ),
        (
            "اطلاعات ویژه",
            {
                "classes": ("collapse",),
                "fields": (
                    "is_active",
                    "is_verify",
                    "is_pin",
                    "categories",
                ),
            },
        ),
        (
            "تاریخ ها",
            {
                "classes": ("collapse",),
                "fields": (
                    "write_date",
                    "update_date",
                    "verify_date",
                    "delete_date",
                ),
            },
        ),
    )


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "description")
