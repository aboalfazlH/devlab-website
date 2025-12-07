from django.views.generic import TemplateView,View
from django.contrib import messages
from django.shortcuts import render
from apps.accounts.models import CustomUser
from .models import Category
from django.http import JsonResponse

class MainPageView(TemplateView):
    template_name = "index.html"


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
