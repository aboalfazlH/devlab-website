from django.contrib import admin
from .models import LinkModel


@admin.register(LinkModel)
class LinkModelAdmin(admin.ModelAdmin):
    """Admin View for LinkModel"""

    list_display = ("name",)
