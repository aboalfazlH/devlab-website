from django.db import models
from django.utils import timezone
from apps.accounts.models import CustomUser

class Question(models.Model):
    """Model definition for Question."""

    def question_upload_path(instance, filename):
        now = timezone.now()
        return f"qa/questions/thumbnails/{now.year}{now.month}{now.day}/{filename}"
    
    name = models.CharField(verbose_name="نام", max_length=110)
    help_image = models.ImageField(
        verbose_name="تصویر کمکی", blank=True, null=True, upload_to=question_upload_path
    )
    question_description = models.TextField(
        verbose_name="توضیحات سوال", blank=True, null=True
    )
    is_active = models.BooleanField(verbose_name="فعال", default=True)
    solved = models.BooleanField(verbose_name="حل شده", default=False)
    is_pin = models.BooleanField(verbose_name="ویژه", default=False)
    write_date = models.DateTimeField(verbose_name="تاریخ مطرح شدن", auto_now_add=True)
    solve_date = models.DateTimeField(verbose_name="تاریخ حل شدن",blank=True,null=True)

    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    def solve(self):
        self.solve_date = timezone.now()
        self.solved = True

    class Meta:
        """Meta definition for Question."""

        verbose_name = "سوال"
        verbose_name_plural = "سوالات"

    def __str__(self):
        """Unicode representation of Question."""
        return f"{self.name}"


class Answer(models.Model):
    """Model definition for Answer."""
    def answer_upload_path(instance, filename):
        now = timezone.now()
        return f"qa/answer/thumbnails/{now.year}{now.month}{now.day}/{filename}"

    name = models.TextField(max_length=110, verbose_name="نام")
    help_image = models.ImageField(
        verbose_name="تصویر کمکی", blank=True, null=True, upload_to=answer_upload_path
    )
    answer_description = models.TextField(
        verbose_name="توضیحات پاسخ", blank=True, null=True
    )
    is_active = models.BooleanField(verbose_name="فعال", default=True)
    is_best = models.BooleanField(verbose_name="بهترین", default=False)
    write_date = models.DateTimeField(verbose_name="تاریخ مطرح شدن", auto_now_add=True)

    class Meta:
        """Meta definition for Answer."""

        verbose_name = "پاسخ"
        verbose_name_plural = "پاسخ ها"

    def __str__(self):
        """Unicode representation of Answer."""
        return f"{self.name}"

    class Meta:
        """Meta definition for Answer."""

        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self):
        """Unicode representation of Answer."""
        pass
