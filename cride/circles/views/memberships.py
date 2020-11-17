"""Circle Membership Views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404

# Models
from cride.circles.models import Circle, Membership

# Serializers
from cride.circles.serializers import MembershipModelSerializer

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions import IsActiveCircleMember


class MembershipViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet,
):
    # el circulo no viene en la url, el circulo (slug_name) esta en el primer nivel de la url
    # y deberia estar en todas las demas
    """Circulo Membership View Set"""

    # queremos que cada vez que se esta validando esta vista queremos que el circulo este
    # disponible a toda la clase y usaremos el metodo dispatch
    # se encarga de las peticiones

    serializer_class = MembershipModelSerializer
    def dispatch(self, request, *args, **kwargs):
        """Verify that circles exists."""
        slug_name=kwargs['slug_name']    
        # este slug_name viene de la url
        self.circle = get_object_or_404(
            # indicamos que el objeto que vamos a obtener es el circulo
            Circle, slug_name=slug_name
        )
        return super(MembershipViewSet, self).dispatch(request, *args, **kwargs)

    # traeremos mos miembro del circulo
    def get_queryset(self):
        """Return circle member."""
        return Membership.objects.filter(
            circle= self.circle,
            is_activate=True,
        )
# reescribiremos el metodo get_permissions para asignar los permisos de acceso a cada accion
# en este caso de que se quiera eliminar miembros del circulo, solo lo podra hacer el admin
    def get_permissions(self):
        """Assing permission based on action"""
        permissions = [IsAuthenticated, IsActiveCircleMember]
        return [p() for p in permissions]

# reescribimos el metodo get_objects, para traer el objecto atra ves del username y no del pk
    def get_object(self):
        """return the circle member by using the user's username"""
        return get_object_or_404(
            Membership,
            user__username= self.kwargs['pk'],
            circle = self.circle,
            is_activate= True,
        )

# esta accion nos permite desactivar el miembro del circulo y asi no podra acceder al detalle    
    def perform_destroy(self, instance):
        instance.is_activate= False
        instance.save()
# cuando se elimina un detalle de usuario del circulo, lo que hacemos en este metodo
# es poner al usuario inactivo, lo quehara que no tenga permisos de acceder al circulo

    