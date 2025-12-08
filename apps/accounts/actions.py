from django.utils import timezone
from datetime import timedelta
from django.contrib import admin, messages
from apps.subscription.models import Subscription,SubscriptionPlan


@admin.action(description="فعال کردن اشتراک طلایی 30 روزه")
def gold_sub_30_day(modeladmin, request, queryset):
    for obj in queryset:
        Subscription.objects.create(
            subscription_plan=SubscriptionPlan.objects.get(real_name="gold"),
            subscription_user=obj,
            start_date=timezone.now(),
            end_date=timezone.now()+timedelta(30),
        )


actions = [gold_sub_30_day]
