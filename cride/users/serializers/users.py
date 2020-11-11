""" Users Serializers"""
# LOS SERIALIZERS NOS SIRVEN PARA CREAR COSAS, LISTAR COSAS Y ACTUALIZAR COSAS(OBJESTOS)
# Django
from django.conf import settings
from django.contrib.auth import authenticate, password_validation
# traemos este metodo para autenticar los campos de login
from django.core.mail import EmailMultiAlternatives
# importamos la propiedad de django para enviar emails de confirmacion alternativos (en este caso emails html)
from django.core.validators import RegexValidator
# importamos esta propiedas que nos ayuda a renderear un template con sus propiedades
from django.template.loader import render_to_string
from django.utils import timezone

# Django RF
from rest_framework import serializers
from  rest_framework.authtoken.models import Token
# importamos el token authentication
from rest_framework.validators import UniqueValidator

# Models
from cride.users.models import User, Profile

#Utilies
import jwt
from datetime import timedelta

# crearemos nuestro primer model form serializer(buscar informacion de para que es este)
# creamos un serializer basado en el modelo de usuario de Django
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
            'phone_number',
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
        # el metodo authenticate nos eregresa email y password a la variable user
        if not user:
            raise serializers.ValidationError('Invalid Credentials')
        # usamos el metodo raise para enviar los errores que sucedieron al validar los datos

        # vamos a hacer que los email sean verificados
        # se verifican enviando un email y luego validandolo  
        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet')
        # en caso de tener errores ValidationError saca el error con este mensaje
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
    email= serializers.EmailField(
        validators= [
            UniqueValidator(queryset= User.objects.all())]
        # no podemos tener dos usuarios con el mismo email
    )
    username= serializers.CharField(
        min_length=4,
        max_length=20,
        validators= [
            UniqueValidator(queryset= User.objects.all())]
        # validamos que no hayan dos usuarios con el mismo username
    )

    # Datos extra
    phone_regex = RegexValidator(
        regex= r'\+?1?\d{9,15}$', # esta expresion dice, puede empezar con signo +
        # o puede empezar con un digito 1 y debe tener de 9 a 15 digitos
        message= " phone number must be entered in the format: +999  up to 15 digits allowed"
    )
    phone_number = serializers.CharField(validators=[phone_regex], max_length = 17)

    password = serializers.CharField(min_length=8,max_length=64)
    password_confirmation= serializers.CharField(min_length=8,max_length=64)

    first_name = serializers.CharField(min_length=2,max_length=30)
    last_name = serializers.CharField(min_length=2,max_length=30)

    # validacion para que los password coincidan
    def validate(self, data):
        """Verified Password match."""
        passwd= data['password']
        passwd_conf= data ['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError('password dont match')
        # queremos que django valide el password las demas validaciones van por serializers
        password_validation.validate_password(passwd)
        return data
# al momento de crear el usuario tambien se crea el perfil
    def create(self, data):
        """Handle user and profile creation."""
        data.pop('password_confirmation')
        #excluimos el password confirmation que no lo necesitamos a la hora de crear el circulo
        user = User.objects.create_user(**data, is_verified=False)
        # creamos un usuario en el objeto del model User
        Profile.objects.create(user=user)
        # creamos un perfil con la informacion del usuario
        self.send_confirmation_email(user)
        # usamos este metodo para verificar el email haciendo uso del usuario
        return user
    
    def send_confirmation_email(self, user):
        """Send account Verification link yo given user"""
        verification_token= self.gen_verification_token(user)
        # creamos un token de verificacion para el usuario
        # generamos un token con JWT este token generado carga informacion en:
        # header, payload y firma criptografica
        # en el payload ponemos a quien pertenece el token y para que se usa
        
        # estos campos provienen de la clae EmailMultivariable(revisar doc)         
        subject= 'Welcome @{}! Verify your account to start using comparte ride'.format(user.username)
        from_email= 'Comparte Ride <noreply@comparteride.com>'
        # este campo nos ayuda a rfenderear el template del html para el email
        content = render_to_string(
            # aca vivira el template
            'emails/users/account_verification.html',
            # enviamos como contexto el token del usuario
            {'token': verification_token, 'user':user}
        )
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        # se envia un mensaje con los datos indicados
        msg.attach_alternative(content, "text/html")
        # agrega el html
        msg.send()
        # envia
    # crearemos nuestro token con jwt que recibe: jwt.encode({'some': 'payload'}, 'secret', algorithm='HS256')
    def gen_verification_token(self, user):
        """Create JWT token that the user can use verify  its account"""
        # utilizaremos expiracion de token, el token dura 15 dias.
        exp_date = timezone.now() + timedelta(days=15)
        payload={
            'user': user.username,
            'exp': int(exp_date.timestamp()),
            'type': 'email_confirmation',
        }
        token= jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return token.decode()
        # retornamos el token y lo transformamos de bits a string

# creamos este serializer para la verificacion de la cuenta
class AccountVerificationSerializer(serializers.Serializer):
    """Account Verification Serializer"""
    
    token = serializers.CharField()
    # debemos validar este campo, debemos hacer el decode del token
    def validate_token(self, data):
        """Verify token is valid"""
        # debemos listar las excepciones posibles a la hora de validar el token
        try:
            payload= jwt.decode(data, settings.SECRET_KEY, algorithms= 'HS256')
            # realizamos el DECODE del token
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired')
        # esta excepcion valida si el token no se ah expirado
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid Token') 
        if payload ['type'] != 'email_confirmation':
            # esta excepcion valida que el type de token sea igual al generado
            raise serializers.ValidationError('Invalid Token')
        self.context['payload'] = payload
        # a la data de paiload le agregamos el payload que contiene el token
        
        return data 
        # retornamos la data del request payload

# reescribimos el metodo save()
    def save(self): 
        """Update users verify status"""
        payload = self.context['payload']
        user = User.objects.get(username= payload['user'])
        # a la variable user= buscamos el username que tiene el token con el usuario que lo creo
        user.is_verified = True
        user.save()
       
