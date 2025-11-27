from django.db import models
from apps.accounts.models import CustomUser
from django.utils import timezone


class SubscriptionPlan(models.Model):
    """Model definition for SubscriptionPlan."""

    plan_name = models.CharField(verbose_name="")
    price = models.PositiveIntegerField(verbose_name="")

    class Meta:
        """Meta definition for SubscriptionPlan."""

        verbose_name = "پلن اشتراک"
        verbose_name_plural = "پلن های اشتراک"

    def __str__(self):
        """Unicode representation of SubscriptionPlan."""
        return self.plan_name


class Subscription(models.Model):
    """Model definition for Subscription."""

    subscription_plan = models.ForeignKey(
        SubscriptionPlan, on_delete=models.CASCADE, verbose_name="پلن اشتراک"
    )
    subscription_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="کاربر"
    )
    start_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ شروع")
    end_date = models.DateTimeField(verbose_name="تاریخ پایان")

    @property
    def is_active(self):
        return self.end_date >= timezone.now()

    class Meta:
        """Meta definition for Subscription."""

        verbose_name = "اشتراک"
        verbose_name_plural = "اشتراک ها"
    def save(self, *args, **kwargs):
        if Subscription.objects.filter(
            subscription_user=self.subscription_user,
            end_date__gte=timezone.now()
        ).exclude(pk=self.pk).exists():
            raise ValueError("این کاربر یک اشتراک فعال دارد و نمی‌تواند اشتراک جدید بگیرد.")

    def __str__(self):
        """Unicode representation of Subscription."""
        return f"{self.subscription_user}-{self.subscription_plan}|{self.start_date} تا {self.end_date}"
