from django.contrib import admin
from .models import Question, Answer
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Question)
class QuestionAdmin(SummernoteModelAdmin):
    """Admin View for Question"""

    list_display = (
        "name",
        "is_active",
        "solved",
        "is_pin",
        "write_date",
        "solve_date",
    )
    summernote_fields = ("question_description",)
    list_filter = (
        "is_active",
        "solved",
        "is_pin",
        "write_date",
        "solve_date",
    )
    readonly_fields = ("write_date", "solve_date")
    search_fields = ("name", "question_description")
    date_hierarchy = "write_date"
    ordering = ("-write_date", "-solve_date")
    autocomplete_fields = ("categories","author")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "question_description",
                    "author",
                ),
            },
        ),
        (
            "اطلاعات پیشرفته",
            {
                "fields": (
                    "is_active",
                    "solved",
                    "is_pin",
                    "categories",
                ),
            },
        ),
        (
            "تاریخ ها",
            {
                "fields": (
                    "write_date",
                    "solve_date",
                ),
            },
        ),
    )


@admin.register(Answer)
class AnswerAdmin(SummernoteModelAdmin):
    """Admin View for Answer"""

    list_display = (
        "__str__",
        "is_active",
        "is_best",
        "write_date",
    )
    summernote_fields = ("answer_description",)
    list_filter = (
        "is_active",
        "is_best",
        "write_date",
    )
    readonly_fields = ("write_date",)
    search_fields = ("answer_description",)
    date_hierarchy = "write_date"
    ordering = ("-write_date",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "answer_description",
                    "is_active",
                    "is_best",
                )
            },
        ),
    )

