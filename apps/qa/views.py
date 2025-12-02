from django.views.generic import ListView,DetailView
from .models import Question,Answer


class QuestionListView(ListView):
    model = Question
    template_name = "questions.html"
    context_object_name = "questions"
    paginate_by = 50
    ordering = "-write_date"

    def get_queryset(self):
        return Question.objects.filter(is_active=True).order_by("solved","is_pin")


class QuestionDetailView(DetailView):
    model = Question
    template_name = "question_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "question"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["answers"] = Answer.objects.filter(
            question=self.object,
        ).order_by("-write_date")
        return context
