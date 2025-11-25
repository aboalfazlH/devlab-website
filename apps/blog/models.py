from django.db import models
from django.utils import timezone
from apps.accounts.models import CustomUser

class Article(models.Model):
    """Model definition for Article."""

    def thumbnail_upload_path(instance, filename):
        """thumbnail upload path"""
        now = timezone.now()
        return f"blog/thumbnails/{now.year}{now.month}{now.day}/{filename}"

    title = models.CharField(max_length=110, verbose_name="موضوع")
    thumbnail = models.ImageField(
        verbose_name="تصویر بندانگشتی",
        upload_to=thumbnail_upload_path,
        blank=True,
        null=True,
    )
    short_description = models.CharField(max_length=110, verbose_name="توضیحات کوتاه")
    description = models.TextField(verbose_name="توضیحات", blank=True, null=True)
    is_active = models.BooleanField(verbose_name="فعال", default=True)
    is_verify = models.BooleanField(verbose_name="تائید شده", default=False)
    is_pin = models.BooleanField(verbose_name="ویژه", default=False)
    author = models.ForeignKey(CustomUser,verbose_name="نویسنده",on_delete=models.CASCADE)
    @property
    def status(self):
        if self.is_active and self.is_verify and self.is_pin:
            return "فعال✅📌"
        elif self.is_active and self.is_verify:
            return "فعال✅"
        elif self.is_active:
            return "فعال❌"
        else:
            return "غیر فعال"

    write_date = models.DateTimeField(verbose_name="تاریخ نوشتن", auto_now_add=True)
    update_date = models.DateTimeField(verbose_name="تاریخ تغییر", auto_now=True)
    delete_date = models.DateTimeField(verbose_name="تاریخ حذف", blank=True, null=True)
    verify_date = models.DateTimeField(
        verbose_name="تاریخ تائید", blank=True, null=True
    )

    class Meta:
        """Meta definition for Article."""

        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def soft_delete(self):
        self.delete_date = timezone.now()
        self.is_active = False
        self.is_verify = False
        self.is_pin = False
    def get_absolute_url(self):
        from django.urls import reverse
        return #reverse('', kwargs={'pk': self.pk})
    def verify(self):
        self.verify_date = timezone.now()
        self.is_verify = True

    def __str__(self):
        """Unicode representation of Article."""
        return f"{self.title}"
