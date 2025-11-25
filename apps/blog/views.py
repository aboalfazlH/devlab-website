from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from .models import Article
from .forms import ArticleForm
from django.http import HttpResponseForbidden
from django.utils.timezone import now
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render


class ArticleListView(ListView):
    model = Article
    template_name = "articles.html"
    context_object_name = "articles"
    paginate_by = 25
    ordering = "-write_date"

    def get_queryset(self):
        return Article.objects.filter(is_active=True).order_by("-is_pin", "-write_date")


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "write_article.html"
    success_url = reverse_lazy("core:home-page")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        today = now().date()
        articles_today = Article.objects.filter(
            author=request.user, write_date__date=today
        )

        if articles_today.count() >= 10 and not (
            self.request.user.is_superuser
            or self.request.user.groups.filter(name="نویسندگان").exists()
        ):

            return HttpResponseForbidden(
                "شما اجازه نوشتن بیشتر از 10 مقاله در روز را ندارید."
            )

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    form_class = ArticleForm
    model = Article
    template_name = "update_article.html"
    context_object_name = "article"
    slug_url_kwarg = "slug"
    slug_field = "slug"
    success_url = reverse_lazy("blog:articles")

    def form_valid(self, form):
        messages.success(self.request, "تغییرات شما ثبت شد✅")
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            messages.error(request, "شما نمی توانید این مقاله را تغییر دهید")
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)


class ArticleDetailView(DetailView):
    model = Article
    template_name = "article_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "article"


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = "article_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "article"
    success_url = reverse_lazy("blog:articles")

    def get(self, request, *args, **kwargs):
        article = self.get_object()
        return render(request, self.template_name, {"article": article})

    def dispatch(self, request, *args, **kwargs):
        article = self.get_object()
        if not request.user.is_superuser and not request.user == article.author:
            return HttpResponseForbidden("نمیتونی حذف کنی!")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        article = self.get_object()

        if request.user.is_superuser:
            article.delete()
            messages.success(request, "حذف شد")
        elif request.user == article.author:
            article.soft_delete()
            messages.success(request, "حذف شد")
        return redirect(self.success_url)
