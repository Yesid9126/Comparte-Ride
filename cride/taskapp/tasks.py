"""vamos a crear una tarea en celery, la tarea es la de envio de email y generacion de token"""

""" en el serializer de usuario, tenemos una funcion que envia un email para poder,
realizar un login, vamos a traer esta funcion para implementarla como una tarea de celery
"""

# Django
# importamos esta propiedas que nos ayuda a renderear un template con sus propiedades
# el template que estamos rendereando es el de email donde se envia el token
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
# importamos la propiedad de django para enviar emails de confirmacion alternativos (en este caso emails html)
from django.conf import settings
# importamos los settings que tienen las configuraciones de celery en desarrollo y produccion

# Models
from cride.users.models import User
#Utilies
import jwt
from datetime import timedelta
import time

# Celery
from celery.decorators import task

def gen_verification_token(user):
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
@task(name= 'send_confirmation_email', max_retries=3)
# task tiene mas atributos como por ej a que funcion debe llamar cuando termine la tarea etc
# una de las buenas practicas es no estar enviando tipos de datos complejos como objetos
# por esa razon enviaremos un id.
# el decorador le agrega a la tarea que se aplique de manera asincrona
# tenemos diferentes formas de llamar una tarea asincrona,hay dos opciones:
# 1- apply_async(args(kwargs)): tiene funcionalidades como
# aplazar la tarea, iniciarla a cierta hora, cuando funcione que luego use otra funcion
def send_confirmation_email(user_pk):
        """Send account Verification link yo given user"""
        
        user= User.objects.get(pk=user_pk)
        verification_token= gen_verification_token(user)
        # la variable verification_token: contiene el token de verificacion de la funcion
        # gen_verification_token, este token de verificacion lo generamos con JWT
        
        # estos campos provienen de la clae EmailMultivariable(revisar doc)         
        subject= 'Welcome @{}! Verify your account to start using comparte ride'.format(user.username)
        from_email= 'Comparte Ride <noreply@comparteride.com>'
        # este campo nos ayuda a rfenderear el template del html para el email
        content = render_to_string(
            # aca vivira el template, usamos un template para el envio de email
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
    