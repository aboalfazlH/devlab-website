from django.contrib import admin
from .models import ApiModel

@admin.register(ApiModel)
class ApiModelAdmin(admin.ModelAdmin):
    '''Admin View for ApiModel'''

    list_display = ('api_name','user','create_date','revoked_date')
    list_filter = ('create_date','revoked_date')
    autocomplete_fields = ('user',)
    readonly_fields = ('create_date',)
    date_hierarchy = 'create_date'
    ordering = ('create_date',)

    def log_addition(self, request, obj, message):
        pass

    def log_change(self, request, obj, message):
        pass

    def log_deletion(self, request, obj, object_repr):
        pass