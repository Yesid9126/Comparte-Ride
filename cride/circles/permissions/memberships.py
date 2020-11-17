"""Cricles permissions classes"""
"""En este permiso vamos a permitir el acceso al circulo, solo de los miembros activos del mismo"""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from cride.circles.models import Membership

class IsActiveCircleMember(BasePermission):
    """Allow access only to circle member.
    
    expect that views implementing this permission have
    a "circle" attribute assing."""

    def has_permission(self, request, view):
        """Verify user is an active member of the circle"""
        circle = view.circle 
# haremos un query que busque un membership,con este usuario,con este circulo y que este activo.
        try:
            Membership.objects.get(
                user= request.user,
                circle= view.circle,
                is_activate=True,
            )
        except Membership.DoesNotExist:
            return False
        return True

# debemos conectar el permiso a la vista dependiendo lA ACCION, en este caso vamos a
# utilizar las acciones retrieve y destroy, que nos permitira buscar o eliminar circulos
# de un determinado usuario