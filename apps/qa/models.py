from django.utils.html import strip_tags
from django.db import models
from django.db.models import Count
from django.utils import timezone
from django.urls import reverse
from apps.accounts.models import CustomUser
from apps.core.models import BaseLike, BaseDisLike, Category




def upload_to_question(instance, filename):
    now = timezone.now()
    return f"qa/questions/{now:%Y/%m/%d}/{filename}"


class Question(models.Model):
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

    categories = models.ManyToManyField(Category, related_name="questions", verbose_name="دسته‌بندی‌ها")

    @property
    def stats(self):
        return (
            Question.objects.filter(id=self.id)
            .annotate(
                likes_count=Count("likes"),
                dislikes_count=Count("dislikes"),
            )
            .values("likes_count", "dislikes_count")
            .first()
        )

    @property
    def likes_count(self):
        return self.stats["likes_count"]

    @property
    def dislikes_count(self):
        return self.stats["dislikes_count"]

    @property
    def score(self):
        return self.likes_count - self.dislikes_count

    def solve(self):
        self.solved = True
        self.solve_date = timezone.now()
        self.save(update_fields=["solved", "solve_date"])

    def get_absolute_url(self):
        return reverse("qa:question-detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "سوال"
        verbose_name_plural = "سوالات"
        ordering = ["-write_date"]

    def __str__(self):
        return self.name


class Answer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    answer_description = models.TextField("توضیحات پاسخ", blank=True, null=True)
    is_active = models.BooleanField("فعال", default=True)
    is_best = models.BooleanField("بهترین", default=False)
    write_date = models.DateTimeField("تاریخ مطرح شدن", auto_now_add=True)

    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )

    @property
    def stats(self):
        return (
            Answer.objects.filter(id=self.id)
            .annotate(
                likes_count=Count("likes"),
                dislikes_count=Count("dislikes"),
            )
            .values("likes_count", "dislikes_count")
            .first()
        )

    @property
    def likes_count(self):
        return self.stats["likes_count"]

    @property
    def dislikes_count(self):
        return self.stats["dislikes_count"]

    @property
    def score(self):
        return self.likes_count - self.dislikes_count

    class Meta:
        verbose_name = "پاسخ"
        verbose_name_plural = "پاسخ‌ها"
        ordering = ["write_date"]

    def __str__(self):
        description = strip_tags(self.answer_description or "")
        if len(description) > 50:
            return f"{description[:50]}..."
        return description


class QLike(BaseLike):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="likes"
    )

    class Meta:
        verbose_name = "لایک"
        verbose_name_plural = "لایک‌ها"
        constraints = [
            models.UniqueConstraint(
                fields=["question", "user"], name="unique_user_like_question"
            )
        ]

    def __str__(self):
        return f"{self.user} liked {self.question}"


class QDisLike(BaseDisLike):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="dislikes"
    )

    class Meta:
        verbose_name = "دیس‌لایک"
        verbose_name_plural = "دیس‌لایک‌ها"
        constraints = [
            models.UniqueConstraint(
                fields=["question", "user"], name="unique_user_dislike_question"
            )
        ]

    def __str__(self):
        return f"{self.user} disliked {self.question}"


class ALike(BaseLike):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["answer", "user"], name="unique_user_like_answer"
            )
        ]

    def __str__(self):
        return f"{self.user} liked {self.answer}"


class ADisLike(BaseDisLike):
    answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, related_name="dislikes"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["answer", "user"], name="unique_user_dislike_answer"
            )
        ]

    def __str__(self):
        return f"{self.user} disliked {self.answer}"
