from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import render
from apps.accounts.models import CustomUser


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
