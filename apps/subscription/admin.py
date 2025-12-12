from django.contrib import admin
from .models import Subscription, SubscriptionPlan


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Admin View for Subscription"""

    list_display = ("subscription_plan", "subscription_user", "start_date", "end_date")
    list_filter = ("subscription_plan", "start_date", "end_date")
    search_fields = ("subscription__user_username", "subscription_user__get_full_name")
    date_hierarchy = "start_date"
    ordering = ("-end_date",)
    def log_addition(self, request, obj, message):
        pass
    def log_change(self, request, obj, message):
        pass
    def log_deletion(self, request, obj, object_repr):
        pass

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    """Admin View for SubscriptionPlan"""

    list_display = ("plan_name", "price","value")
    list_filter = ("price",)
    search_fields = ("plan_name",)
    ordering = ("-value",)
    def log_addition(self, request, obj, message):
        pass
    def log_change(self, request, obj, message):
        pass
    def log_deletion(self, request, obj, object_repr):
        pass