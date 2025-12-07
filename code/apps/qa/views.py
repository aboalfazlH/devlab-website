from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib import messages
from .models import Question, Answer, QLike, QDisLike,ALike,ADisLike
from .forms import QuestionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse


# Question views
class QuestionListView(ListView):
    model = Question
    template_name = "questions.html"
    context_object_name = "questions"
    paginate_by = 50
    ordering = "-write_date"

    def get_queryset(self):
        return Question.objects.filter(is_active=True).order_by("solved", "is_pin")


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


class QuestionCreateView(LoginRequiredMixin, CreateView):
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
            return HttpResponseForbidden("شما نمی‌توانید بیش از 50 سوال در روز بپرسید.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user

        if form.instance.slug in ["question", "ask"]:
            form.add_error("slug", "این شناسه در دسترس نیست")
            return self.form_invalid(form)
        return super().form_valid(form)

    # TODO: if user has subscribe can ask 100 question and 1 question in month pin


class QuestionUpdateView(UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = "question_update.html"

    def dispatch(self, request, *args, **kwargs):
        question = self.get_object()
        if not request.user.is_superuser and request.user != question.author:
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


class QuestionLikeView(View):
    def post(self, request, slug):
        q = Question.objects.get(slug=slug)

        QDisLike.objects.filter(user=request.user, question=q).delete()

        like, created = QLike.objects.get_or_create(user=request.user, question=q)
        if created:
            messages.success(request, "نظر شما با موفقیت ثبت شد")
        else:
            messages.info(request, "شما قبلاً لایک داده‌اید")

        return redirect("qa:questions")


class QuestionDisLikeView(View):
    def post(self, request, slug):
        q = Question.objects.get(slug=slug)

        QLike.objects.filter(user=request.user, question=q).delete()

        dislike, created = QDisLike.objects.get_or_create(user=request.user, question=q)
        if created:
            messages.success(request, "نظر شما با موفقیت ثبت شد")
        else:
            messages.info(request, "شما قبلاً دیسلایک داده‌اید")

        return redirect("qa:questions")


# Answer views
class AnswerCreateView(View):
    def post(self, request, slug):
        question = get_object_or_404(Question, slug=slug)
        content = request.POST.get("content")

        if not content:
            messages.error(request, "متن پاسخ نباید خالی باشد.")
            return redirect(question.get_absolute_url())

        Answer.objects.create(
            question=question, user=request.user, answer_description=content
        )

        messages.success(request, "پاسخ شما ثبت شد.")
        return redirect(question.get_absolute_url())


class AnswerUpdateView(UpdateView):
    model = Answer
    template_name = "edit_answer.html"
    fields = ["answer_description"]
    pk_url_kwarg = "pk"

    def get_success_url(self):
        question_slug = self.object.question.slug
        return reverse("qa:question-detail", kwargs={"slug": question_slug})


class AnswerDeleteView(LoginRequiredMixin, View):
    def post(self, request, slug, pk):
        answer = get_object_or_404(Answer, id=pk)

        if request.user == answer.user or request.user.is_superuser:
            answer.delete()
            messages.success(request, "پاسخ حذف شد.")
        else:
            messages.error(request, "شما اجازه حذف این پاسخ را ندارید.")

        return redirect("qa:question-detail", slug=slug)


class AnswerBestView(LoginRequiredMixin, View):
    def post(self, request, slug, pk):
        question = Question.objects.get(slug=slug)
        answer = get_object_or_404(Answer, id=pk)

        if Answer.objects.filter(
            question=question, is_active=True, is_best=True
        ).exists():
            messages.error(request, "این سوال یک پاسخ به عنوان بهترین دارد")
            return redirect("qa:question-detail", slug=slug)

        if request.user == question.author or request.user.is_superuser:
            answer.is_best = not answer.is_best
            answer.save()
            if answer.is_best:
                messages.success(request, "پاسخ به عنوان بهترین پاسخ انتخاب شد.")
            else:
                messages.success(request, "پاسخ دیگر بهترین نیست.")
        else:
            messages.error(
                request, "شما اجازه ندارید این پاسخ را به عنوان بهترین انتخاب کنید."
            )

        return redirect("qa:question-detail", slug=slug)


class AnswerLikeView(View):
    def post(self, request, pk, slug):
        a = Answer.objects.get(pk=pk)

        ADisLike.objects.filter(user=request.user, answer=a).delete()

        like, created = ALike.objects.get_or_create(user=request.user, answer=a)
        if created:
            messages.success(request, "نظر شما با موفقیت ثبت شد")
        else:
            messages.info(request, "شما قبلاً لایک داده‌اید")

        return redirect("qa:question-detail",slug=slug)


class AnswerDisLikeView(View):
    def post(self, request, pk,slug):
        a = Answer.objects.get(pk=pk)

        ALike.objects.filter(user=request.user, answer=a).delete()

        dislike, created = ADisLike.objects.get_or_create(user=request.user, answer=a)
        if created:
            messages.success(request, "نظر شما با موفقیت ثبت شد")
        else:
            messages.info(request, "شما قبلاً دیسلایک داده‌اید")

        return redirect("qa:question-detail",slug=slug)
