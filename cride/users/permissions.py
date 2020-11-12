"""User Permissions."""

# Djanfo REST FRamework
from rest_framework.permissions import BasePermission

class IsAccountOwner(BasePermission):
    """Allow access only to objects owned by the requesting user."""
# este permiso lo otorgaremos para la accion retieve
    def has_object_permission(self, request, view, obj):
        """Check object and user are the same"""
        return request.user == obj

# este permiso nos permite ingresar a la vista que esta utilizando el verbo retrieve