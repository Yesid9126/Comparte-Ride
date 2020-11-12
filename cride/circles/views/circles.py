"""Circles views."""
""" crearemos las vistas para los circulos, usaremos la viste Viewset
la cual nos sirve para lista, crear, y eliminar circulos, esta vista
tiene en su interior todos los mixins(create,update,retrive etc) los mixins hacen todo
el trabajo de crear o listar o consultar o eliminar """
# revisar la documentacion de los mixins para ver que metodos usa y si en algun momento
# se pueden reescribir

# Django REST framework
from rest_framework import mixins, viewsets
# importamos la clase viewset que hara todas las funciones

# Serializers
from cride.circles.serializers import CircleModelSerializer

# Models
from cride.circles.models import Circle, Membership

# Permission
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions import IsCircleAdmin


# esta vista nos permitira crear,listar y actualizar circulos
# esta vista maneja todos los metods(GET,POST,PUT,PATCH,DELETE)
# como los viewset contienen todos los mixins para litar, crear , eliminar
# vamos a excluir el de eliminar para que nadie pueda eliminar el circulo
class CircleViewSet(viewsets.mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet): 
    """Circle Viewset"""

    queryset = Circle.objects.all()
    # buscara todos los circulos existentes
    serializer_class = CircleModelSerializer 
    # colocamos permisos con IsAuthenticated
    # permission_classes = (IsAuthenticated,)
    lookup_field = 'slug_name'
    # indicamos con que valor en la url se buscara el circulo
    # anterioemnte lo haciamos con el id, ahora se busca con el slug_name

    
# despues de validar la autenticacion de un usuario debemos otorgar el permiso
# vamos a otorgar permiso de ingreso a la vista con el metodo IsAuthenticated

# como tenemos circulos privados y publicos debemos reescribir el metodo queryset
# para que  la momento de listar los circulos estos solo nos traigan los publicos
    def get_queryset(self):
        """Restrict list to public only"""
        queryset = Circle.objects.all()
        # trae todos los circulos disponibles
        if self.action == 'list':
            # si la accion que realizamos es listar entonces filtramos por los que tengan is_public=True
            return queryset.filter(is_public=True)
            # retorna los circulos que son publicos
        return queryset

# vamos a reescribir un metodo para los permisos de esta vista, este permiso esta basado en acciones
# dependiendo la accion tiene permisos de administrador o usuario
# recordemos que esta vista nos da acceso para listar, crear, eliminar circulos
# por eso necesitamos que solo los administradores tengan permiso de actualizar
# esta funcion proviene de viewset
    def get_permissions(self):
        """Assing permissions based on action"""
        permissions =[IsAuthenticated]
        # por default el usuario debe estar autenticado
        if self.action in ['update', 'partial_update']:
            # si la accion es update o partial_update
            permissions.append(IsCircleAdmin)
            # agregamos a permission el permiso IsCircleAdmin
        return [permission() for permission in permissions]

# vamos a poner la funcionalidad para cuando se cree un circulo, el miembro que lo creo
# sea el administrador, ademas pondremos si el circulo tiene limite se debe indicar cual es
# vamos a buscar un metodo para sobreescribir,en la documentacion de ModelViewset
# utilizaremos la clase de createmodelmixin para crear un circulo
    def perform_create(self, serializer):
        """Assing circle admin."""
        circle = serializer.save()
        # salvamos el serializer del circulo, despues de que haya validado todos los datos
        user = self.request.user
        # traemos el usuario que esta en el login y que creara el circulo y lo asignamos a campo user
        profile = user.profile
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
    
    

    