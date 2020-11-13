""" users views """

# Django REST framework
from rest_framework.views import APIView
from rest_framework.response import Response
# importamos el response de DRF
from rest_framework import status, viewsets, mixins
# importamos los status para ser usados en este caso HTTP_201_CREATED
from rest_framework.decorators import action
# traemos los actions

# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from cride.users.permissions import IsAccountOwner

# Serializers
from cride.users.serializers.profiles import ProfileModelSerializer
from cride.circles.serializers import CircleModelSerializer
from cride.users.serializers import (
    UserLoginSerializer ,UserModelSerializer,UserSingUpSerializer,
    AccountVerificationSerializer,
)

# Models
from cride.users.models import User, Profile
from cride.circles.models import Circle


# vamos a cambiar nuestras vistas a viewsets en esta tendremos:views actions(list,create,destoy)
# usaremos las urls con routers
# podemos crear acciones, las acciones se dividen en acciones de detalle y de no detalle

class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,  
                  viewsets.GenericViewSet,):
    """User Viewset.
    
    Handle Singup, login an Account verification.
    """
# cada que usemos un Retievemixin debemos configurar un queryset base a partir del cual se va a hacer
# el query del detalle
# este es el detalle de usuario
    
    queryset = User.objects.filter(is_active=True, is_client=True) 
    # traemos los usuarios que tengan is_active=True y is_client=True
    # quesryset contiene los usuarios que tienen el filtro indicado
    serializer_class = UserModelSerializer
    lookup_field = 'username'
    # en vez de poner el id en la url pondra el username del usuario.

# haremos que solo el usuario pueda acceder a su detalle de usuario
    def get_permissions(self):
        """Assing permissions based on action"""
        if self.action in ['singup', 'login', 'verify']:
            permissions =[AllowAny]
    # cualquiera que vaya a acceder a estas peticiones lo podra hacer
# si la accion es de tipo retrieve se debe validar el permiso de acceso
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        # si no hay ninguna opcion debe tener una sesion autenticada 
        return [p() for p in permissions]
    

    # la primera accion no es de detalle por que es de signup
    @action(detail=False, methods=['post'])
    # el metodo que vamos a crear debe llevar el nimbre que tendra en la url
    # reemplazamos este metodo por la vista anterior para login
    def login(self, request):
        """User Login"""
        import pdb; pdb.set_trace()
        serializer = UserLoginSerializer(data = request.data)
        # el serializer contiene todos los datos del login y los valida
        serializer.is_valid(raise_exception= True)
    # este comando nos valida los datos que ingresamos
# lo que queremos es que al momento de save el serializer nos devuelva un token y el usuario
    
        user, token = serializer.save()
    # este campo genera un token

        # a la data del request agregamos estos dos campos
        data = {
            'user':UserModelSerializer(user).data,
            # serializer puede recibir una instancia de un objeto y mostrarlo
            # aca mostraria todos los datos del user definidos en el UserModelSerializer
            'access token': token
        }
        return Response (data, status=status.HTTP_201_CREATED)
# status viene de la documentacion de status del codigo 201, debemos importar status

    @action(detail= False, methods=['post'])
    def signup (self, request):
        """User signup."""
        serializer = UserSingUpSerializer(data = request.data)
        serializer.is_valid(raise_exception= True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response (data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Account Verification"""
        serializer = AccountVerificationSerializer(data = request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        data = {'message':'Congratulations, Welcome CRIDE'}
        return Response (data, status=status.HTTP_200_OK)

# vamos a traer el detalle del perfil, para esto utilizaremos el action=True
    @action(detail=True, methods=['put', 'patch'])
    def profile (self, request, *args, **kwargs):
        """Update profile data."""
        # traemos el usuario
        user = self.get_object()
        profile = user.profile
        partial = request.method == 'PATCH'
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data= UserModelSerializer(user).data
        return Response(data)

# vamos a traer los circulos en los cuales esta registrado un usuario, para esto vamos a realizar
# un retrive por lo que tenemos que utilizar el mixin que nos permite hacer retrive
# lo que haremos es traer los datos del modelo de circulos
    def retrieve(self, request, *args, **kwargs):
        """Extra data to the response."""
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        circles = Circle.objects.filter(
            members= request.user,
            # a members le asignamos el usuario
            membership__is_activate= True,
            # y buscamos los memberships que esten activos
            )
        data={
            'user':response.data,
            'circles': CircleModelSerializer(circles,many=True).data

        }
        response.data = data
        return response