from apps.core.models import BaseLink
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from apps.subscription.models import Subscription
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.db import models
from . import validators


class ProfileLink(BaseLink):
    """link for profile"""

    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "لینک"
        verbose_name_plural = "لینک ها"

    def __str__(self):
        return f"{self.link_type} ی {self.user}"


class CustomUser(AbstractUser):
    """CustomUser model"""

    def avatar_upload_path(instance, filename):
        """thumbnail upload path"""
        now = timezone.now()
        return f"auth/avatars/{now.year:04}{now.month:02}{now.day:02}/{filename}"

    # Unique fields
    email = models.EmailField(unique=True, verbose_name=_("email"))
    phone_number = models.CharField(
        verbose_name="شماره تلفن",
        max_length=15,
        unique=True,
        blank=True,
        null=True,
        validators=[validators.validate_phone_number],
    )

    # Personal info
    avatar = models.ImageField(
        verbose_name=_("avatar"),
        upload_to=avatar_upload_path,
        default="auth/avatars/20251204/person.png",
    )
    about = models.CharField(
        max_length=200, verbose_name="درباره کاربر", blank=True, null=True
    )
    bio = models.TextField(verbose_name="بیوگرافی", blank=True, null=True)

    # Links
    git_account = models.URLField(
        verbose_name="حساب گیت هاب/گیت لب",
        validators=[validators.validate_git_url],
        blank=True,
        null=True,
    )
    website = models.URLField(verbose_name="سایت", blank=True, null=True)

    facebook = models.URLField(
        verbose_name="فیس بوک",
        blank=True,
        null=True,
        validators=[validators.validate_facebook_link],
    )

    instagram = models.URLField(
        verbose_name="اینستاگرام",
        blank=True,
        null=True,
        validators=[validators.validate_instagram_link],
    )

    linkedin = models.URLField(
        verbose_name="لینکدین",
        blank=True,
        null=True,
        validators=[validators.validate_linkedin_link],
    )

    telegram = models.URLField(
        verbose_name="تلگرام",
        blank=True,
        null=True,
        validators=[validators.validate_telegram_link],
    )

    # Booleans
    public_article = models.BooleanField(
        verbose_name="مقاله عمومی",
        help_text="با این گزینه،پست های شما عمومی محسوب شده و قابل استفاده توسط دیگران است",
        default=False,
    )

    # Public fields
    public_email = models.EmailField(verbose_name="ایمیل عمومی", blank=True, null=True)

    public_phone_number = models.EmailField(
        verbose_name="شماره تلفن عمومی", blank=True, null=True
    )

    # Meta
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("phone_number", "username")

    # Properties
    @property
    def has_link(self):
        """Check User Profile has link"""
        links = [
            self.git_account,
            self.website,
            self.facebook,
            self.instagram,
            self.linkedin,
            self.telegram,
            ProfileLink.objects.filter(user=self).exists(),
        ]
        return any(links)

    @property
    def subscribe_status(self):
        now = timezone.now()
        subs = Subscription.objects.filter(subscription_user=self).order_by("-end_date")

        if not subs.exists():
            return "بدون سابقه اشتراک❔"

        latest = subs.first()
        if latest.end_date > now:
            return "اشتراک فعال✅"
        else:
            return "اشتراک منقضی شده❌"

    def get_absolute_url(self):
        """Get User Detail"""
        from django.urls import reverse

        return reverse("users-profile", kwargs={"username": self.username})

    def __str__(self):
        """Str for user model"""
        full_name = self.get_full_name().strip()
        return full_name if full_name else self.username
