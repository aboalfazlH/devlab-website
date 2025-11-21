from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserChangeForm,CustomUserCreationForm

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin View for CustomUser"""

    list_display = ('id','username','get_full_name','is_active','is_staff','is_superuser')
    list_display_links = ('id','username')
    list_editable = ('is_active','is_staff','is_superuser')
    list_filter = ('is_active','is_staff','is_superuser','date_joined','last_login')
    readonly_fields = ('date_joined','last_login')
    search_fields = ('username','get_full_name')
    date_hierarchy = 'date_joined'
    ordering = ('last_login','date_joined','first_name','last_name','id',)