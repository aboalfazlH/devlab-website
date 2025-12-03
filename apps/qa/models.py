from apps.accounts.models import CustomUser
from django.db import models
from django.utils import timezone
from django.urls import reverse


def upload_to_question(instance, filename):
    """Generate dynamic upload path for question thumbnails."""
    now = timezone.now()
    return f"qa/questions/{now:%Y/%m/%d}/{filename}"



class Question(models.Model):
    """Represents a question submitted by users."""

    name = models.CharField("نام", max_length=110)
    help_image = models.ImageField(
        "تصویر کمکی", blank=True, null=True, upload_to=upload_to_question
    )
    question_description = models.TextField("توضیحات سوال", blank=True, null=True)
    is_active = models.BooleanField("فعال", default=True)
    solved = models.BooleanField("حل شده", default=False)
    is_pin = models.BooleanField("ویژه", default=False)

    write_date = models.DateTimeField("تاریخ مطرح شدن", auto_now_add=True)
    solve_date = models.DateTimeField("تاریخ حل شدن", blank=True, null=True)

    slug = models.SlugField("شناسه", unique=True)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="questions"
    )

    def solve(self):
        """Mark question as solved and set solve timestamp."""
        self.solved = True
        self.solve_date = timezone.now()
        self.save(update_fields=["solved", "solve_date"])

    def get_absolute_url(self):
        """Return URL for detailed view of the question."""
        return reverse("qa:question-detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "سوال"
        verbose_name_plural = "سوالات"
        ordering = ["-write_date"]

    def __str__(self):
        return self.name


class Answer(models.Model):
    """Represents an answer submitted for a question."""

    name = models.CharField("نام", max_length=110)
    answer_description = models.TextField("توضیحات پاسخ", blank=True, null=True)
    is_active = models.BooleanField("فعال", default=True)
    is_best = models.BooleanField("بهترین", default=False)

    write_date = models.DateTimeField("تاریخ مطرح شدن", auto_now_add=True)
    slug = models.SlugField("شناسه", unique=True)

    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )

    class Meta:
        verbose_name = "پاسخ"
        verbose_name_plural = "پاسخ‌ها"
        ordering = ["write_date"]

    def __str__(self):
        return self.name
