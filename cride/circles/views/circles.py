"""Circles views."""
""" crearemos las vistas para los circulos, usaremos la viste Viewset
la cual nos sirve para lista, crear, y eliminar circulos, esta vista
tiene en su interior todos los mixins(create,update,retrive etc) los mixins hacen todo
el trabajo de crear o listar o consultar o eliminar """
# revisar la documentacion de los mixins para ver que metodos usa y si en algun momento
# se pueden reescribir

# Django REST framework
from rest_framework import viewsets
# importamos la clase viewset que hara todas las funciones
from rest_framework.permissions import IsAuthenticated

# Serializers
from cride.circles.serializers import CircleModelSerializer

# Models
from cride.circles.models import Circle, Membership


# esta vista nos permitira crear,listar y actualizar circulos
# esta vista maneja todos los metods(GET,POST,PUT,PATCH,DELETE)
class CircleViewSet(viewsets.ModelViewSet):
    """Circle Viewset"""

    queryset = Circle.objects.all()
    # buscara todos los circulos existentes
    serializer_class = CircleModelSerializer 
    # luego traemos el srializer para validar los datos
    permission_classes = (IsAuthenticated,)
    
# despues de validar la autenticacion de un usuario debemos otorgar el permiso
# vamos a otorgar permiso de ingreso a la vista con el metodo IsAuthenticated

# como tenemos circulos privados y publicos debemos reescribir el metodo queryset
# para que  la momento de listar los circulos estos solo nos traigan los publicos
    def get_queryset(self):
        """Restrict listo to public only"""
        queryset = Circle.objects.all()
        # trae todos los circulos disponibles
        if self.action == 'list':
            # si la accion que realizamos es listar entonces filtramos por los que tengan is_public=True
            return queryset.filter(is_public=True)
            # retorna los circulos que son publicos
        return queryset

# vamos a poner la funcionalidad para cuando se cree un circulo, el miembro que lo creo
# sea el administrador, ademas pondremos si el circulo tiene limite se debe indicar
# vamos a buscar un metodo para sobreescribir,en la documentacion de ModelViewset
# utilizaremos la clase de createmodelmixin para crear un circulo
    def perform_create(self, serializer):
        """Assing circle admin."""
        circle = serializer.save()
        # salvamos el serializer del circulo, despues de que haya validado todos los datos
        user = self.request.user
        # traemos el usuario que esta en el login y que creara el circulo y lo asignamos a campo user
        profile = self.user.profile
        # a la variable profile le enviamos el perfil de usuario que creara el circulo
        Membership.objects.create(
            user= user,
            profile=profile,
            circle=circle,
            is_admin=True,
            remaining_invitations = 10,
        )
        # creamos un objeto membership y utilizamos los campos definidos en el modelo de membership
        return super().perform_create(serializer)
    
    

    