from django.urls import reverse
from django.db import models
from django.utils import timezone
from apps.accounts.models import CustomUser
from django.template.defaultfilters import slugify
from unidecode import unidecode
from apps.core.models import BaseCategory, BaseComment
import re


class ArticleCategory(BaseCategory):
    """Article Category model"""
    content = models.TextField(verbose_name="توضیحات برچسب",blank=True,null=True)
    slug = models.SlugField(verbose_name="شناسه")

    class Meta:
        verbose_name = "برچسب"
        verbose_name_plural = "برچسب ها"

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
    views = models.PositiveIntegerField(default=0, verbose_name="بازدید")
    short_description = models.CharField(max_length=110, verbose_name="توضیحات کوتاه")
    description = models.TextField(verbose_name="توضیحات", blank=True, null=True)
    is_active = models.BooleanField(verbose_name="فعال", default=True)
    is_verify = models.BooleanField(verbose_name="تائید شده", default=False)
    is_pin = models.BooleanField(verbose_name="ویژه", default=False)
    author = models.ForeignKey(
        CustomUser, verbose_name="نویسنده", on_delete=models.CASCADE
    )
    slug = models.SlugField(
        verbose_name="شناسه",
        unique=True,
    )

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

    @property
    def most_visited(self):
        return self.views >= 1000

    write_date = models.DateTimeField(verbose_name="تاریخ نوشتن", auto_now_add=True)
    update_date = models.DateTimeField(verbose_name="تاریخ تغییر", auto_now=True)
    delete_date = models.DateTimeField(verbose_name="تاریخ حذف", blank=True, null=True)
    verify_date = models.DateTimeField(
        verbose_name="تاریخ تائید", blank=True, null=True
    )
    categories = models.ManyToManyField(ArticleCategory)

    class Meta:
        """Meta definition for Article."""

        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def soft_delete(self):
        self.delete_date = timezone.now()
        self.is_active = False
        self.is_verify = False
        self.is_pin = False
        self.save()

    def get_absolute_url(self):
        return reverse("blog:article-detail", kwargs={"slug": self.slug})

    def verify(self):
        self.verify_date = timezone.now()
        self.is_verify = True
        self.save()

    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":
            text = unidecode(self.title)
            text = re.sub(r"[^\w\s-]", "", text)
            text = re.sub(r"[-\s]+", "-", text)
            base_slug = text.lower().strip("-_")

            if not base_slug:
                base_slug = "article"

            slug = base_slug
            counter = 1

            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        """Unicode representation of Article."""
        return f"{self.title}"
