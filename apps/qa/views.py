from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Question,Answer
from .forms import QuestionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy

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


class QuestionCreateView(LoginRequiredMixin,CreateView):
    model = Question
    template_name = "write_question.html"
    form_class = QuestionForm

    def dispatch(self, request, *args, **kwargs):
        
        today = now().date()
        questions_today = Question.objects.filter(
            author=request.user, write_date__date=today
        )
        if questions_today.count() >= 50 and not (
            request.user.is_superuser
            or request.user.groups.filter(name="نویسندگان").exists()
        ):
            return HttpResponseForbidden(
                "شما نمی‌توانید بیش از 50 سوال در روز بپرسید."
            )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        
        if form.instance.slug in ["question","ask"]:
            form.add_error("slug","این شناسه در دسترس نیست")
            return self.form_invalid(form)
        return super().form_valid(form)

    # TODO: if user has subscribe can ask 100 question and 1 question in month pin


class QuestionUpdateView(UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = "question_update.html"

    def dispatch(self, request, *args, **kwargs):
        question = self.object
        article = self.get_object()
        if not request.user.is_superuser and request.user != article.author:
            return HttpResponseForbidden("شما اجازه حذف این سوال را ندارید.")
        return super().dispatch(request, *args, **kwargs)

class QuestionDeleteView(DeleteView):
    model = Question
    template_name = "question_delete.html"
    context_object_name = "question"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("qa:questions")

    def dispatch(self, request, *args, **kwargs):
        article = self.get_object()
        if not request.user.is_superuser and request.user != article.author:
            return HttpResponseForbidden("شما اجازه حذف این مقاله را ندارید.")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        question = self.get_object()
        question.delete()
        return redirect(self.success_url)
