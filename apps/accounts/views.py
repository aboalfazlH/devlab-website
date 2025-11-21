from .forms import CustomUserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import CustomUser

class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('admin:index') #  TODO : ADD LOGIN AND A TRUE SUCCESS URL
    template_name = "sign-up.html"