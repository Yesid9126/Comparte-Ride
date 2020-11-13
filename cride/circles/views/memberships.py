"""Circle Membership Views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404

# Models
from cride.circles.models import Circle, Membership

# Serializers
from cride.circles.serializers import MembershipModelSerializer


class MembershipViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
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
    