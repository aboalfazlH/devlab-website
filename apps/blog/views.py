from django.views.generic import ListView, CreateView,DetailView
from .models import Article
from .forms import ArticleForm
from django.http import HttpResponseForbidden
from django.utils.timezone import now
from django.urls import reverse_lazy
from django.contrib import messages


class ArticleListView(ListView):
    model = Article
    template_name = "articles.html"
    context_object_name = "articles"
    paginate_by = 25
    ordering = "-write_date"

    def get_queryset(self):
        return Article.objects.filter(is_active=True).order_by("-is_pin", "-write_date")


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "write_article.html"
    success_url = reverse_lazy("core:home-page")

    def dispatch(self, request, *args, **kwargs):
        today = now().date()
        articles_today = Article.objects.filter(
            author=request.user, write_date__date=today
        )

        if articles_today.count() >= 10:
            return HttpResponseForbidden(
                "شما اجازه نوشتن بیشتر از 10 مقاله در روز را ندارید."
            )

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleDetailView(DetailView):
    model = Article
    template_name = "article_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "article"