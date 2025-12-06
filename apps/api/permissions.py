from rest_framework.permissions import BasePermission
import hashlib
from .models import ApiModel


class HasValidApiToken(BasePermission):
    """
    Permission class to validate incoming API tokens.
    If the token is valid, the ApiModel instance is attached
    to request.api_entry for further access.
    """

    def has_permission(self, request, view):
        token = view.kwargs.get("token")
        if not token:
            return False

        hashed = hashlib.sha256(token.encode()).hexdigest()

        try:
            api_entry = ApiModel.objects.get(token=hashed, is_active=True)
        except ApiModel.DoesNotExist:
            return False

        # Attach api_entry to request for use in views
        request.api_entry = api_entry
        return True
