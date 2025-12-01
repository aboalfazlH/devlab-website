from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
import re
from django.core.exceptions import ValidationError
from apps.core.models import BaseLink

class CustomUser(AbstractUser):
    def avatar_upload_path(instance, filename):
        """thumbnail upload path"""
        now = timezone.now()
        return f"auth/avatars/{now.year}{now.month}{now.day}/{filename}"

    def validate_git_url(value):
        """Validate that the URL is from github.com or gitlab.com"""
        pattern = r"^https?://(www\.)?(github\.com|gitlab\.com)/.+$"
        if not re.match(pattern, value):
            raise ValidationError("لینک باید فقط از github.com یا gitlab.com باشد.")

    def validate_facebook_link(value):
        pattern = r"^https?:\/\/(www\.)?facebook\.com\/[A-Za-z0-9_.-]+\/?$"
        if not re.match(pattern, value):
            raise ValidationError("فقط لینک معتبر Facebook وارد کنید.")

    def validate_instagram_link(value):
        pattern = r"^https?:\/\/(www\.)?instagram\.com\/[A-Za-z0-9_.-]+\/?$"
        if not re.match(pattern, value):
            raise ValidationError("فقط لینک معتبر Instagram وارد کنید.")

    def validate_linkedin_link(value):
        pattern = (
            r"^https?:\/\/(www\.)?linkedin\.com\/(in|company)\/[A-Za-z0-9_.-]+\/?$"
        )
        if not re.match(pattern, value):
            raise ValidationError("فقط لینک معتبر لینکدین وارد کنید.")

    def validate_telegram_link(value):
        pattern = r"^https?:\/\/(t\.me)\/[A-Za-z0-9_]{5,32}$"
        if not re.match(pattern, value):
            raise ValidationError(
                "فقط لینک معتبر Telegram وارد کنید. مثال: https://t.me/username"
            )

    email = models.EmailField(unique=True, verbose_name=_("email"))
    avatar = models.ImageField(
        verbose_name=_("avatar"), upload_to=avatar_upload_path, blank=True, null=True
    )
    about = models.CharField(
        max_length=200, verbose_name="درباره کاربر", blank=True, null=True
    )
    bio = models.TextField(verbose_name="بیوگرافی", blank=True, null=True)
    phone_number = models.CharField(
        verbose_name="شماره تلفن", max_length=15, blank=True, null=True
    )
    git_account = models.URLField(
        verbose_name="حساب گیت هاب/گیت لب",
        validators=[validate_git_url],
        blank=True,
        null=True,
    )
    website = models.URLField(verbose_name="سایت", blank=True, null=True)
    facebook = models.URLField(
        verbose_name="فیس بوک",
        blank=True,
        null=True,
        validators=[validate_facebook_link],
    )
    instagram = models.URLField(
        verbose_name="اینستاگرام",
        blank=True,
        null=True,
        validators=[validate_instagram_link],
    )
    linkedin = models.URLField(
        verbose_name="لینکدین",
        blank=True,
        null=True,
        validators=[validate_linkedin_link],
    )
    telegram = models.URLField(
        verbose_name="تلگرام",
        blank=True,
        null=True,
        validators=[validate_telegram_link],
    )

    public_article = models.BooleanField(
        verbose_name="مقاله عمومی",
        help_text="با این گزینه،پست های شما عمومی محسوب شده و قابل استفاده توسط دیگران است",
        default=False,
    )

    public_email = models.EmailField(verbose_name="ایمیل عمومی",blank=True,null=True)
    public_phone_number = models.EmailField(verbose_name="شماره تلفن عمومی",blank=True,null=True)
    @property
    def has_link(self):
        links = [
            self.git_account,
            self.website,
            self.facebook,
            self.instagram,
            self.linkedin,
            self.telegram,
        ]
        return any(links)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("users-profile", kwargs={"username": self.username})

    def __str__(self):
        return (
            f"{self.username}" if self.get_full_name() is None else self.get_full_name()
        )

class ProfileLink(BaseLink):
    """link for profile"""
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    class Meta:
        verbose_name = "لینک"
        verbose_name_plural = "لینک ها"

    def __str__(self):
        return f"{self.link_type} {self.user}"