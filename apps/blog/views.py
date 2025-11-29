from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.timezone import now
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import JsonResponse

from .models import Article, ArticleCategory, ArticleComment
from .forms import ArticleForm


class ArticleListView(ListView):
    model = Article
    template_name = "articles.html"
    context_object_name = "articles"
    paginate_by = 25
    ordering = "-write_date"

    def get_queryset(self):
        return Article.objects.filter(is_active=True).order_by("-is_pin", "-write_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ArticleCategory.objects.annotate(
            article_count=Count("articles", filter=Q(articles__is_active=True))
        ).order_by("-article_count")
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "write_article.html"
    success_url = reverse_lazy("blog:articles")

    def dispatch(self, request, *args, **kwargs):
        today = now().date()
        articles_today = Article.objects.filter(
            author=request.user, write_date__date=today
        )
        if articles_today.count() >= 10 and not (
            request.user.is_superuser
            or request.user.groups.filter(name="Writers").exists()
        ):
            return HttpResponseForbidden(
                "شما نمی‌توانید بیش از ۱۰ مقاله در روز بنویسید."
            )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "update_article.html"
    context_object_name = "article"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("blog:articles")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            messages.error(request, "شما اجازه تغییر این مقاله را ندارید.")
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "تغییرات شما ذخیره شد✅")
        return super().form_valid(form)


class ArticleDetailView(DetailView):
    model = Article
    template_name = "article_detail.html"
    context_object_name = "article"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        session_key = f"viewed_article_{obj.id}"
        if not self.request.session.get(session_key, False):
            obj.views += 1
            obj.save(update_fields=["views"])
            self.request.session[session_key] = True
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = ArticleComment.objects.filter(
            article=self.object, comment__isnull=True
        ).order_by("-write_date")
        return context


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = "article_delete.html"
    context_object_name = "article"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("blog:articles")

    def dispatch(self, request, *args, **kwargs):
        article = self.get_object()
        if not request.user.is_superuser and request.user != article.author:
            return HttpResponseForbidden("شما اجازه حذف این مقاله را ندارید.")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        article = self.get_object()
        if request.user.is_superuser:
            article.delete()
        else:
            article.soft_delete()
        messages.success(request, "حذف مقاله موفق بود")
        return redirect(self.success_url)


class ArticlePinView(LoginRequiredMixin, View):
    def post(self, request, slug, *args, **kwargs):
        article = get_object_or_404(Article, slug=slug)
        if not request.user.is_superuser:
            return HttpResponseForbidden("شما اجازه سنجاق کردن مقاله را ندارید.")
        article.is_pin = not article.is_pin
        article.save()
        return redirect("blog:article-detail", slug=slug)


class ArticleFilterWithCategory(ListView):
    model = Article
    template_name = "articles.html"
    context_object_name = "articles"
    paginate_by = 25
    ordering = "-write_date"

    def get_queryset(self):
        slug = self.kwargs.get("category")
        return Article.objects.filter(categories__slug=slug, is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = get_object_or_404(ArticleCategory, slug=self.kwargs.get("category"))
        context["categories"] = ArticleCategory.objects.annotate(
            article_count=Count("articles", filter=Q(articles__is_active=True))
        ).order_by("-article_count")
        return context


class CategoryAutocomplete(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")
        qs = ArticleCategory.objects.filter(name__icontains=query)[:10]
        results = [{"id": c.id, "text": c.name} for c in qs]
        return JsonResponse({"results": results})


class CommentDetailView(DetailView):
    model = ArticleComment
    template_name = "comment_detail.html"
    context_object_name = "comment"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment"] = get_object_or_404(
            ArticleComment,
            id=self.kwargs["pk"],
            comment__isnull=True,
            is_active=True
        )
        context["article"] = get_object_or_404(Article, slug=self.kwargs["slug"])
        return context


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        content = request.POST.get("content")
        parent_id = request.POST.get("parent_comment")

        if not content:
            messages.error(request, "متن کامنت نباید خالی باشد.")
            return redirect(article.get_absolute_url())

        if parent_id:
            parent = get_object_or_404(ArticleComment, id=parent_id, article=article)
            ArticleComment.objects.create(
                article=article,
                user=request.user,
                content=content,
                comment=parent,
            )
        else:
            ArticleComment.objects.create(
                article=article,
                user=request.user,
                content=content,
            )

        messages.success(request, "نظر شما ثبت شد.")
        return redirect(article.get_absolute_url())


class CommentDeleteView(LoginRequiredMixin, View):
    def post(self, request, slug, comment_id):
        comment = get_object_or_404(ArticleComment, id=comment_id)

        if request.user == comment.user or request.user.is_superuser:
            comment.delete()
            messages.success(request, "کامنت حذف شد.")
        else:
            messages.error(request, "شما اجازه حذف این کامنت را ندارید.")

        return redirect("blog:article-detail", slug=slug)
