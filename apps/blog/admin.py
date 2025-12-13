from django.contrib import messages
from django.contrib import admin
from .models import Article, ArticleComment
from django import forms


class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "class": "quill-editor",
                    "style": "display:none;",
                }
            ),
        }
    def log_addition(self, request, obj, message):
        pass
    def log_change(self, request, obj, message):
        pass
    def log_deletion(self, request, obj, object_repr):
        pass

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Admin View for Article"""

    form = ArticleAdminForm
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
    autocomplete_fields = (
        "author",
        "categories",
    )
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
    list_per_page = 50
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


    @admin.action(description="حذف نرم مقاله ")
    def soft_delete(modeladmin, request, queryset):
        for obj in queryset:
            obj.soft_delete()
        count = len(queryset)
        messages.success(request, f"حذف نرم {count} مقاله موفق بود")

    actions = ["soft_delete",]
    
    class Media:
        js = ("static/js/quill-init.js",)

    def log_addition(self, request, obj, message):
        pass
    def log_change(self, request, obj, message):
        pass
    def log_deletion(self, request, obj, object_repr):
        pass



@admin.register(ArticleComment)
class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ("id",)
    search_fields = ("id",)
    def log_addition(self, request, obj, message):
        pass
    def log_change(self, request, obj, message):
        pass
    def log_deletion(self, request, obj, object_repr):
        pass

    def save_model(self, request, obj, form, change):
        if obj.is_pin:
            obj.pin()
        else:
            super().save_model(request, obj, form, change)