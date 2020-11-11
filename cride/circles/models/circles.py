"""modelo de circulos """
# Django
from django.db import models
# aca importamos la clase de modelos de django

# Utilities
from cride.utils.models import CRideModel
# aca importamos el modelo que indica los datos de creacion y modificacion

# creamos nuestra clase(modelo) que hereda de la clase bastracta
class Circle(CRideModel):
    """ un circulo es un grupo privado donde los rides se ofrecen y toman
    para unirte a un circulo debe ser con una invitacion de un mienbro
    perteneciente al circulo"""

    name = models.CharField('circle name', max_length = 140)
    slug_name = models.SlugField(unique=True, max_length= 40)
    # este va a ser el "username" que se usara en el grupo y debe ser unico
    about = models.CharField('circles description',max_length= 255)
    # esta es la descripcion del grupo
    picture= models.ImageField(upload_to ='circles/pictures/', blank= True, null=True)
# manytomany nos sirve para referenciar un campo con otro modelo
    members = models.ManyToManyField(
        # la referencia es a:
        'users.User',
        #lo hacemos a tra ves de :
         through='circles.Membership',
         # a traves de que campos se hace la relacion al usuario
         through_fields= ('circles', 'user')
         )
# cuando utilizamos el modelo de membership saldra un error ya que tenemos varias llaves
# foraneas(foreingkey) debemos especificar cual usar

    # estadisticas por cada circulo(rides tomados y ofrecidos)
    rides_offered = models.PositiveIntegerField(default=0)
    rides_taken = models.PositiveIntegerField(default=0)

    # este campo nos verificara si el circulo es oficial de la pagina
    verified = models.BooleanField(
        'verified circle',
        default = False,
        help_text= 'verificacion de circulos oficiales de la pagina'
    )

    # este campo nos permite saber que circulos son privados
    # si es pubico y esta cerrado es por que ya tiene el limite de miembros
    is_public= models.BooleanField(
        default = True,
        help_text='listado de circulos publicos para acceder'
    )

    # este campo nos permite si el grupo tiene limite de miembros y cuanto es
    is_limited = models.BooleanField(
        'limited',
        default=False, # por default ningun circulo esta limitado
        help_text= 'limite de miembros por este circulo'

    )
    member_limit = models.PositiveIntegerField(
        default = 0,
        help_text ='este circulo esta limitado por una cantidad de miembros'
    )

    # este es el string que regresara cuando tengamos la instancia de modelo
    def __str__(self):
        return self.name

# queremos utilizar la clase META creada en utils/models.py, esto lo hacemos para no tener,
# que importarla desde este modulo, y podemos modificarla para que al momento de hacer object.all
# nos ordene los circulos por la cantidad de rides ofrecidos o rides tomados
class Meta(CRideModel.Meta):

    ordering = ['-rides_taken', '-rides_offered']
# traemos los datos de manera descendente con el -, y 1 traemos los rides tomados
# luego traemos los circulos con los rides offered
    