from django.utils import timezone
from datetime import timedelta
from django.contrib import admin, messages
from apps.subscription.models import Subscription, SubscriptionPlan


@admin.action(description="فعال کردن اشتراک برنزی 30 روزه")
def bronze_sub_30_day(modeladmin, request, queryset):
    for obj in queryset:
        Subscription.objects.create(
            subscription_plan=SubscriptionPlan.objects.get(real_name="bronze"),
            subscription_user=obj,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(30),
        )
    count = len(queryset)
    messages.success(request, f"فعال کردن {count} اشتراک برنزی موفق بود")


@admin.action(description="فعال کردن اشتراک نقره ای 30 روزه")
def silver_sub_30_day(modeladmin, request, queryset):
    for obj in queryset:
        Subscription.objects.create(
            subscription_plan=SubscriptionPlan.objects.get(real_name="silver"),
            subscription_user=obj,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(30),
        )
    count = len(queryset)
    messages.success(request, f"فعال کردن {count} اشتراک نقره ای موفق بود")


@admin.action(description="فعال کردن اشتراک طلایی 30 روزه")
def gold_sub_30_day(modeladmin, request, queryset):
    for obj in queryset:
        Subscription.objects.create(
            subscription_plan=SubscriptionPlan.objects.get(real_name="gold"),
            subscription_user=obj,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(30),
        )
    count = len(queryset)
    messages.success(request, f"فعال کردن {count} اشتراک طلایی موفق بود")


@admin.action(description="فعال کردن اشتراک الماسی 30 روزه")
def diamond_sub_30_day(modeladmin, request, queryset):
    for obj in queryset:
        Subscription.objects.create(
            subscription_plan=SubscriptionPlan.objects.get(real_name="diamond"),
            subscription_user=obj,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(30),
        )
    count = len(queryset)
    messages.success(request, f"فعال کردن {count}اشتراک الماسی موفق بود")


actions = [
    bronze_sub_30_day,
    silver_sub_30_day,
    gold_sub_30_day,
    diamond_sub_30_day,
]
