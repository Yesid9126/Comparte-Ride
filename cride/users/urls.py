""" urls de los usuarios"""

#Django
from django.urls import path

# Views
from cride.users.views import (
    UserLoginAPIView,
    UserSingUpAPIView,
    AccountVerificationAPIView,
    )


urlpatterns = [
    path ('users/singup/', UserSingUpAPIView.as_view(), name='singup'),
    # esta url es para hacer el signup de usuarios
    path ('users/login/', UserLoginAPIView.as_view(), name='login'),
    # url para hacer login de usuarios
    path ('users/verify/', AccountVerificationAPIView.as_view(), name= 'verify'),
    # creamos esta url para la verificacion de la cuenta
    
]

# el name='login sirve para cuando se haga el reverse quede como 'users:login'
