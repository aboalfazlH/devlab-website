from django.db.models import Count,Q
from django.http import JsonResponse, HttpResponseForbidden
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    View,
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.utils.timezone import now
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Article, ArticleCategory,ArticleComment
from .forms import ArticleForm


# List all published articles
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
            article_count=Count("articles",filter=Q(articles__is_active=True))
        ).order_by("-article_count")
        return context


# Create a new article (login required)
class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "write_article.html"
    success_url = reverse_lazy("core:home-page")

    def dispatch(self, request, *args, **kwargs):
        """Limit number of articles per user per day."""
        today = now().date()
        articles_today = Article.objects.filter(
            author=request.user, write_date__date=today
        )
        if articles_today.count() >= 10 and not (
            request.user.is_superuser
            or request.user.groups.filter(name="Writers").exists()
        ):
            return HttpResponseForbidden(
                "You cannot write more than 10 articles per day."
            )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Set current user as author before saving."""
        form.instance.author = self.request.user
        return super().form_valid(form)


# Update an existing article
class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "update_article.html"
    context_object_name = "article"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("blog:articles")

    def dispatch(self, request, *args, **kwargs):
        """Check if user is the author before editing."""
        obj = self.get_object()
        if obj.author != request.user:
            messages.error(request, "شما نمی توانید این را تغییر دهید")
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "تغیرات شما ذخیره شد✅")
        return super().form_valid(form)


# View article details
class ArticleDetailView(DetailView):
    model = Article
    template_name = "article_detail.html"
    context_object_name = "article"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        """Increment view count once per session."""
        obj = super().get_object(queryset)
        session_key = f"viewed_article_{obj.id}"
        if not self.request.session.get(session_key, False):
            obj.views += 1
            obj.save(update_fields=["views"])
            self.request.session[session_key] = True
        return obj

    def get_context_data(self, **kwargs):
        """Add comments and form to context."""
        context = super().get_context_data(**kwargs)
        context['comments'] = ArticleComment.objects.filter(article=self.object, comment__isnull=True).order_by('-write_date')
        return context


# Delete an article
class ArticleDeleteView(DeleteView):
    model = Article
    template_name = "article_delete.html"
    context_object_name = "article"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("blog:articles")

    def dispatch(self, request, *args, **kwargs):
        """Allow only author or superuser to delete."""
        article = self.get_object()
        if not request.user.is_superuser and request.user != article.author:
            return HttpResponseForbidden("You cannot delete this article.")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        article = self.get_object()
        if request.user.is_superuser:
            article.delete()
        else:
            article.soft_delete()
        messages.success(request, "حذف مقاله موفق بود")
        return redirect(self.success_url)


# Pin or unpin an article
class ArticlePinView(LoginRequiredMixin, View):
    def post(self, request, slug, *args, **kwargs):
        article = get_object_or_404(Article, slug=slug)
        if not request.user.is_superuser:
            return HttpResponseForbidden(
                "You do not have permission to pin this article."
            )
        article.is_pin = not article.is_pin
        article.save()
        return redirect("blog:article-detail", slug=article.slug)


# Autocomplete for Select2 categories
class CategoryAutocomplete(View):
    def get(self, request, *args, **kwargs):
        """Return JSON response for Select2 AJAX requests."""
        query = request.GET.get("q", "")
        qs = ArticleCategory.objects.filter(name__icontains=query)[:10]
        results = [{"id": c.id, "text": c.name} for c in qs]
        return JsonResponse({"results": results})


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
        context["category"] = ArticleCategory.objects.get(slug=self.kwargs.get("category"))
        context["categories"] = ArticleCategory.objects.annotate(
            article_count=Count("articles",filter=Q(articles__is_active=True))
        ).order_by("-article_count")
        return context
