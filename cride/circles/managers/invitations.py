"""Circle invitations manager"""

""" los managers es una interfaz atraves de la cual se puede acceder a la base de datos 
(realizar busquedas)con operaciones de querys, User.objects.top5(el manager es un top 5 de users)
los managers se acceden atraves de la propiedas Objects de cada clase
y permiten realizar consultas dependiendo el manager definido"""

# Django
from django.db import models

# Utilities
import random
from string import ascii_uppercase, digits
# importamos estas funcionalidades para la creacion de los codigos de invitacion.
# se importan caracteres(ascci_uppercase) y numeros

# Django REST Framework

# este manager sera usado para la creacion de codigos
class InvitationManager(models.Manager):
    """Invitation Manager.
    
    used to handle code creation
    """
    CODE_LENGTH = 10
    # nuestro codigo tendra 10 elementos

    # vamos a crear las invitaciones con conjunto de caracteres aleatorios
    # para esto traemos la propiedad ascci_uppercase
    def create(self, **kwargs):
        """Handle code creation."""
        pool = ascii_uppercase + digits +'.-_'
        # si en los kwargs no viene un codigo, lo debemos crear, y cogemos n elementos
        # desde nuestro pool y lo generamos de manera aleatoria con random
        code = kwargs.get('code', ''.join(random.choices(pool,k= self.CODE_LENGTH)))
        # .join nos junta los caracteres elegidos

        # vamos a validar que no haya un codigo existente igual, mientras no exista generamos uno nuevo
        while self.filter(code=code).exists():
            code = ''.join(random.choices(pool,k= self.CODE_LENGTH))
            # creacion de codigo
        # si se genero el codigo debemos asignarlo a los kwargs
        kwargs ['code']= code

        return super(InvitationManager, self).create(**kwargs)
