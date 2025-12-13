from django.contrib import admin
from .models import (
    Subscription, 
    SubscriptionPlan, 
    DiscountCode, 
    DiscountCodeUsage, 
    DiscountItem, 
    Product,
)


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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'price')
    list_filter = ('product_type',)
    search_fields = ('name',)
    def log_addition(self, request, obj, message):
        pass
    def log_change(self, request, obj, message):
        pass
    def log_deletion(self, request, obj, object_repr):
        pass

class DiscountItemInline(admin.TabularInline):
    model = DiscountItem
    extra = 1
    def log_addition(self, request, obj, message):
        pass
    def log_change(self, request, obj, message):
        pass
    def log_deletion(self, request, obj, object_repr):
        pass

@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'active', 'created_at', 'expires_at')
    inlines = [DiscountItemInline]
    def log_addition(self, request, obj, message):
        pass
    def log_change(self, request, obj, message):
        pass
    def log_deletion(self, request, obj, object_repr):
        pass

@admin.register(DiscountCodeUsage)
class DiscountCodeUsageAdmin(admin.ModelAdmin):
    list_display = ('discount_code', 'user', 'used_at')
    search_fields = ('discount_code__code', 'user__username')
    readonly_fields = ('discount_code', 'user', 'used_at')
    def log_addition(self, request, obj, message):
        pass
    def log_change(self, request, obj, message):
        pass
    def log_deletion(self, request, obj, object_repr):
        pass
    