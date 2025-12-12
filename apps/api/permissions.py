from rest_framework.permissions import BasePermission
import hashlib
from .models import ApiModel


class HasValidApiToken(BasePermission):
    """Validate API token passed in path"""
    def has_permission(self, request, view):
        token = view.kwargs.get("token")
        if not token:
            return False
        hashed = ApiModel.hash_token(token)
        try:
            request.api_entry = ApiModel.objects.get(key=hashed, revoked_date__isnull=True)
            return True
        except ApiModel.DoesNotExist:
            return False