from django.contrib import admin
from .models import LinkModel, Category


@admin.register(LinkModel)
class LinkModelAdmin(admin.ModelAdmin):
    """Admin View for LinkModel"""

    list_display = ("name",)
    search_fields = ("name",)
    def log_addition(self, request, obj, message):
        pass
    def log_change(self, request, obj, message):
        pass
    def log_deletion(self, request, obj, object_repr):
        pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin View for Category"""

    list_display = ("name",)
    search_fields = ("name",)
    def log_addition(self, request, obj, message):
        pass
    def log_change(self, request, obj, message):
        pass
    def log_deletion(self, request, obj, object_repr):
        pass