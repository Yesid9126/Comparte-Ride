""" Users Serializers"""
# Django
from django.contrib.auth import authenticate
# traemos este metodo para autenticar los campos de login

# Django RF
from rest_framework import serializers
from  rest_framework.authtoken.models import Token
# importamos el token authentication

# Models
from cride.users.models import User

# crearemos nuestro primer model form serializer(buscar informacion de para que es este)
class UserModelSerializer(serializers.ModelSerializer):
    """User Model Serializer"""
    class Meta:
        """Meta Class"""
        model = User
        # importamos el modelo de usuario que contiene todos nuestros datos
        fields =(
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number'
        )
        # definiremos los atributos de nuestro serializer

# este serializer nos permite validar los datos para login
class UserLoginSerializer(serializers.Serializer):
    """User Login Serializer"""
    """maneja los datos de sesion de inicio"""

    email= serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)
    #sabemos por los validadores de Django que el password debe ser mayor a 8

    # queremos validar los datos, si no son validos la API respondera el error
    # documentacion de validacion de serializer , se puede hacer por cada campo o por todos los campos
    # reescribimos el metodo validate que correra despues de todas las validaciones principales
    # si algun error se da en esta validacion lanzara una excepcion de tipo serializer
# documentacion serializer validation
    def  validate(self,data):
        """ Check credentials"""
        # utilizamos el metodo autenticate, recibe las credenciales y si son validas regresa el usuario
        # si las credenciales no son validas regresara none
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid Credentials')
        # enviamos los errores que sucedieron al validar los datos
        self.context['user']= user
# context es un atributo de serializer que puede agregar una instancia al objeto
# agregaria al campo user= los datos del usuario
        return data

# reescribimos el metodo create para generar el token
# como en la vista creamos un campo llamado token y le asignamos la salvada de serializer
# osea se verificaron y autenticaron los datos y el campo token contiene la verificacion
    def create(self,data):
        """Generate or retrive token """
# como authtoken tiene en el usuario un onetoonfield significa que solo un usuario puede
# tener un token, entonces generaremos la recuperacion del token en caso de que ya este creado
# o generamos unn nuevo en caso de que no este creado
        token, created = Token.objects.get_or_create(user=self.context['user'])
        # user= trae el objeto de usuario con los campos indicados en UserModelSerializer
# retornaremos el usuario y el token
        return self.context['user'], token.key


# serializer para verificar los datos del SingUp
class UserSingUpSerializer(serializers.Serializer):
    """User Sing Up Serializers"""
    """ Handle sing up data validation and user/profile creation"""