# vamos a extender el modelo de usuario que trae Django por Default
# utilizamos el atributo OneToOneField para que cada campo sea unico
# usamos un modelo personalizado el cual se usa con clase bastracta o con modelo proxy

#Django
from django.db import models
from django.contrib.auth.models import AbstractUser
# importamos la clase abstracta de Django para crear el modelo de usuario
from django.core.validators import RegexValidator
# importamos esta clase para validar el numero de telefono

#utilities
from cride.utils.models import CRideModel # importamos este modelo que contiene la fecha de creacion y modificacion del objeto

class User (CRideModel, AbstractUser):
    # esta clase de usuario hereda de CRideModel y de AbstracUser(contiene los campos de user)
    # este modelo es personalizado y agrega nuevos campos (Fields) al modelo.

    email = models.EmailField(
        'email address',
        unique = True, # no puede haber otro usuario con este mismo valor
        error_messages= {
            'unique':'A user already exist.'
        }
    )

# queremos verificar el numero de telefono y lo haremos con los validators(debemos importarlo)
    phone_regex = RegexValidator(
        regex= r'\+?1?\d{9,15}$', # esta expresion dice, puede empezar con signo +
        # o puede empezar con un digito 1 y debe tener de 9 a 15 digitos
        message= " phone number must be entered in the format: +999  up to 15 digits allowed"
    )
    phone_number = models.CharField(validators=[phone_regex], max_length = 17, blank=True)
    # cada que se guarde el valor el busca el validador en phone_regex

    USERNAME_FIELD= 'email'
    # este campo hara que el ingreso del username sea por su email
    REQUIRED_FIELDS = ['username','first_name','last_name']
    # esta variable define cuales son los campos obligatorios que debe ingresar el ususario

    is_client= models.BooleanField(
        'client',
        default=True,
        help_text = (
            'validamos si un usuario es cliente y/o administrador'
        )
    )
    # este campo nos sirve para validar si el usuario es cliente y/o administrador
    
    is_verified= models.BooleanField(
        'verified',
        default = False, # por default ningun usuario esta verificado
        help_text= 'se valida la verificacion de la cuenta de ususario'
    )
    # este campo nos ayuda a verificar que el usuario valido el correo y la cuenta

    def __str__(self):
        return self.username

    # esta funcion retornara el first_name
    # pero en este caso haremos que nos retorne el username ya que es el campo con el que nos identificamos
    def get_short_name(self):
        return self.username

