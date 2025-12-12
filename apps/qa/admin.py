from django.contrib import admin
from .models import Question, Answer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin View for Question"""

    list_display = (
        "name",
        "is_active",
        "solved",
        "is_pin",
        "write_date",
        "solve_date",
    )
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
    def log_addition(self, request, obj, message):
        pass
    def log_change(self, request, obj, message):
        pass
    def log_deletion(self, request, obj, object_repr):
        pass

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Admin View for Answer"""

    list_display = (
        "__str__",
        "is_active",
        "is_best",
        "write_date",
    )
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

    def log_addition(self, request, obj, message):
        pass
    def log_change(self, request, obj, message):
        pass
    def log_deletion(self, request, obj, object_repr):
        pass