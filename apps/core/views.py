from django.views.generic import TemplateView,View
from apps.accounts.models import CustomUser
from .models import Category
from django.http import JsonResponse
from django.db.models import Q
from apps.blog.models import Article
from apps.qa.models import Question
from apps.pricing.models import SubscriptionPlan
from django.shortcuts import render


class MainPageView(TemplateView):
    template_name = "index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = Article.objects.filter(is_active=True).order_by("-write_date")[:10]
        context["questions"] = Question.objects.filter(is_active=True).order_by("-write_date")[:10]
        context["plans"] = SubscriptionPlan.objects.filter().order_by("-value")[:10]
        return context

class AboutPageView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["personnels"] = CustomUser.objects.filter(groups__name="کارمندان")
        return context


class ContactPageView(TemplateView):
    template_name = "contact.html"


class CategoryAutocomplete(View):
    """Create select2  autocomplete"""

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")
        queryset = Category.objects.filter(name__icontains=query)[:10]
        results = [{"id": category.id, "text": category.name} for category in queryset]
        return JsonResponse({"results": results})


class SearchView(View):
    template_name = "search_results.html"

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")
        results = {}

        if query:
            results["articles"] = Article.objects.filter (
                Q(title__icontains=query) 
                | Q(description__icontains=query)
                | Q(short_description__icontains=query)
                | Q(slug__icontains=query)
            )
            results["questions"] = Question.objects.filter (
                Q(name__icontains=query) 
                | Q(question_description__icontains=query)
            )
            results["users"] = CustomUser.objects.filter (
                Q(username__icontains=query) 
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(about__icontains=query)
                | Q(bio__icontains=query)
            )

        return render(request, self.template_name, {"results": results, "query": query})

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)