from django.views.generic import ListView
from .models import Question,Answer


class QuestionListView(ListView):
    model = Question
    template_name = "questions.html"
    context_object_name = "questions"
    paginate_by = 50
    ordering = "-write_date"

    def get_queryset(self):
        return Question.objects.filter(is_active=True).order_by("solved","is_pin")