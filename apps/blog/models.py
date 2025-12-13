from django.db import models,transaction
from django.urls import reverse
from django.utils import timezone

from unidecode import unidecode
import re

from apps.core.models import Category, BaseComment
from apps.accounts.models import CustomUser


class Article(models.Model):
    """Model representing an article."""

    # File upload path
    def thumbnail_upload_path(instance, filename):
        """Generate upload path for thumbnail images."""
        now = timezone.now()
        return f"blog/thumbnails/{now.year}{now.month}{now.day}/{filename}"

    # Fields
    title = models.CharField(max_length=110, verbose_name="موضوع")
    thumbnail = models.ImageField(
        verbose_name="تصویر بندانگشتی",
        upload_to=thumbnail_upload_path,
        blank=True,
        null=True,
    )
    short_description = models.CharField(max_length=110, verbose_name="توضیحات کوتاه",blank=True,null=True)
    description = models.TextField(verbose_name="توضیحات", blank=True, null=True)
    views = models.PositiveIntegerField(default=0, verbose_name="بازدید")

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

    write_date = models.DateTimeField(verbose_name="تاریخ نوشتن", auto_now_add=True)
    update_date = models.DateTimeField(verbose_name="تاریخ تغییر", auto_now=True)
    delete_date = models.DateTimeField(verbose_name="تاریخ حذف", blank=True, null=True)
    verify_date = models.DateTimeField(
        verbose_name="تاریخ تائید", blank=True, null=True
    )

    categories = models.ManyToManyField(
        Category, related_name="articles", verbose_name="دسته‌بندی‌ها"
    )

    # Meta options
    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
        ordering = ["-write_date"]

    # Properties
    @property
    def status(self):
        """Return a human-readable status of the article."""
        if self.is_active and self.is_verify and self.is_pin:
            return "فعال✅📌"
        elif self.is_active and self.is_verify:
            return "فعال✅"
        elif self.is_active:
            return "فعال❌"
        return "غیر فعال"

    @property
    def most_visited(self):
        """Return True if the article has more than 1000 views."""
        return self.views >= 1000

    # methods
    def soft_delete(self):
        """Soft delete the article by marking it inactive."""
        self.is_active = False
        self.is_verify = False
        self.is_pin = False
        self.delete_date = timezone.now()
        self.save()

    def verify(self):
        """Mark the article as verified."""
        self.is_verify = True
        self.verify_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        """Return the absolute URL to the article detail page."""
        return reverse("blog:article-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        """Auto-generate a unique slug if not provided."""
        if not self.slug or self.slug.strip() == "":
            # Convert title to ASCII-friendly slug
            base_slug = unidecode(self.title)
            base_slug = re.sub(r"[^\w\s-]", "", base_slug)
            base_slug = re.sub(r"[-\s]+", "-", base_slug).lower().strip("-_")
            if not base_slug:
                base_slug = "article"

            slug = base_slug
            counter = 1

            # Ensure slug uniqueness
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    # magic methods
    def __str__(self):
        return self.title


class ArticleComment(BaseComment):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="مقاله")
    comment = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True,related_name='replies')
    write_date = models.DateTimeField(
        auto_now_add=True,
    )
    is_active = models.BooleanField(default=True)
    is_check = models.BooleanField(
        default=False,
    )
    is_pin = models.BooleanField(default=False)

    @property
    def is_reply(self):
        return self.comment is not None

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        constraints = [
            models.UniqueConstraint(
                fields=["article"],
                condition=models.Q(is_pin=True),
                name="unique_pinned_comment_per_article"
            )
        ]
    
    def pin(self):
        """
        Atomically pin this comment.
        If another pinned comment exists for the same article,
        it will be automatically unpinned.
        """
        with transaction.atomic():
            ArticleComment.objects.select_for_update().filter(
                article=self.article,
                is_pin=True
            ).exclude(pk=self.pk).update(is_pin=False)

            self.is_pin = True
            self.save(update_fields=["is_pin"])

    def __str__(self):
        return super().__str__()
