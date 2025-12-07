from django.contrib import admin
from .models import LinkModel, Category


@admin.register(LinkModel)
class LinkModelAdmin(admin.ModelAdmin):
    """Admin View for LinkModel"""

    list_display = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin View for Category"""

    list_display = ("name",)
    search_fields = ("name",)
