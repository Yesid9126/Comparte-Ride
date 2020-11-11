""" users views """

# Django REST framework
from rest_framework.views import APIView
from rest_framework.response import Response
# importamos el response de DRF
from rest_framework import status
# importamos los status para ser usados en este caso HTTP_201_CREATED

# Serializers
from cride.users.serializers import (
    UserLoginSerializer ,UserModelSerializer,UserSingUpSerializer,
    AccountVerificationSerializer,
)

# vista para hacer login
class UserLoginAPIView(APIView):
# reescribimos el metodo post (enviaremos datos , un token) para poder crear el token
# los token nos permiten la autorizacion a la vista
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data = request.data)
        # este token recibe y maneja las peticiones HTTP POST
        serializer.is_valid(raise_exception= True)
    # este comando nos valida los datos que ingresamos
# lo que queremos es que al momento de save el serializer nos devuelva un token y el usuario
    
        user, token = serializer.save()
    # este campo genera un token

        data = {
            'user':UserModelSerializer(user).data,
            # serializer puede recibir una instancia de un objeto y mostrarlo
            # aca mostraria todos los datos del user definidos en el UserModelSerializer
            'access token': token
        }

        return Response (data, status=status.HTTP_201_CREATED)
# status viene de la documentacion de status del codigo 201, debemos importar status

# vista para hacer el Sing Up
class UserSingUpAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSingUpSerializer(data = request.data)
        serializer.is_valid(raise_exception= True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response (data, status=status.HTTP_201_CREATED)

# vista para verificar la cuenta
class AccountVerificationAPIView(APIView):
    """Account verification."""
    def post(self, request, *args, **kwargs):
        serializer = AccountVerificationSerializer(data = request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        data = {'message':'Congratulations, Welcome CRIDE'}
        return Response (data, status=status.HTTP_200_OK)
