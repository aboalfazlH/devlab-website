from django.db import models
from django.utils import timezone


class SubscriptionPlan(models.Model):
    """Model definition for SubscriptionPlan."""

    plan_name = models.CharField(verbose_name="نام پلن")
    price = models.PositiveIntegerField(verbose_name="قیمت",default=0)
    value = models.PositiveIntegerField(verbose_name="ارزش پلن",default=0)

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
        "accounts.CustomUser", on_delete=models.CASCADE, verbose_name="کاربر"
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
        if (
            Subscription.objects.filter(
                subscription_user=self.subscription_user, end_date__gte=timezone.now()
            )
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValueError(
                "این کاربر یک اشتراک فعال دارد و نمی‌تواند اشتراک جدید بگیرد."
            )
        super().save(*args, **kwargs)

    def __str__(self):
        """Unicode representation of Subscription."""
        start = self.start_date.strftime("%Y-%m-%d %H:%M")
        end = self.end_date.strftime("%Y-%m-%d %H:%M")
        return f"{self.subscription_user.get_full_name()} | {self.subscription_plan} | {start} تا {end}"
