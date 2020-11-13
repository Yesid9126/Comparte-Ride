""" model de perfil de usuario"""

# Django 
from django.db import models

# Utilies
from cride.utils.models import CRideModel

# creamos nuestro modelo de perfil

class Profile(CRideModel):
    """ este sera el perfil de usuario"""
    user = models.OneToOneField('users.User', on_delete= models.CASCADE)
    # el primer atributo de un OneToOneField es la clase de la cual heredara
    # este campo nos validara que usuario esta usando el modelo de perfil
    # los campos tipo OneToOneFIeld y Foreignkey deben tener el atributo on_delete
    picture = models.ImageField(
        'profile picture',
        upload_to= 'users/pictures/',
        # indicamos la carpeta donde se guardaran las imagenes
        blank = True,
        null = True,

    )
    # podemos usar imagenes ya que tenemos pillow instalado(requeriments)

    biography = models.TextField(max_length= 500, blank= True)

    # vamos a crear las estadisticas para cada perfil de usuario
    # cuantos rides ha tomado
    rides_taken = models.PositiveIntegerField(default=0)
    # este campo PositiveIntegerField no admite valores negativos

    # cuantos rides ha compartido
    rides_offered = models.PositiveIntegerField(default=0)

    # tenemos una reputacion por ususario
    reputation = models.FloatField(
        default= 5.0,
        help_text= 'Users reputations based on the rides taken offered'
    )

    # representacion en string del usuario
    def __str__(self):
        return str(self.user)
    