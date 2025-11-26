from django.db import models
from apps.accounts.models import CustomUser


class BaseCategory(models.Model):
    """Model definition for Category."""

    name = models.CharField("نام برچسب")
    description = models.TextField("توضیح برچسب")
    

    class Meta:
        """Meta definition for Category."""

        verbose_name = "Category"
        verbose_name_plural = "Categorys"

    def __str__(self):
        """Unicode representation of Category."""
        pass


class BaseComment(models.Model):
    """Model definition for Comment."""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="کاربر")
    content = models.TextField(verbose_name="محتوا")

    class Meta:
        """Meta definition for Comment."""

        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

    def __str__(self):
        """Unicode representation of Comment."""
        return f"نظر شماره {self.id}"
