""" Vamos a crear un permiso de acceso para los administradores de los circulos"""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from cride.circles.models import Membership

# este permiso se otorga a los administradores de los circulos(quien lo crea)
# este permiso permite modificar circulos 
class IsCircleAdmin(BasePermission):
    """allow access only to circle admin"""

    # reescribimos el metodo que nos interesa, este devolvera un True o False
    # dependiendo de si se cumple con las condiciones
    def has_object_permission(self, request, view, obj):
        # el objeto fue el que trajo el viewset, en este caso es el circulo
        """Verify user have a membership in the object."""
        # lo podemos hacer atra ves del objeto membership
        try:
            Membership.objects.get(
            user= request.user,
            circle= obj,
            is_admin= True,
            is_activate = True,
            )
        except Membership.DoesNotExist:
            return False
        return True