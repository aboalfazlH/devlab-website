from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
import re
from django.core.exceptions import ValidationError


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

    @property
    def has_link(self):
        if self.git_account:
            return True

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("users-profile", kwargs={"username": self.username})

    def __str__(self):
        return (
            f"{self.username}" if self.get_full_name() is None else self.get_full_name()
        )
