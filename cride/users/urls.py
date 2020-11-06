""" urls de los usuarios"""

#Django
from django.urls import path

# Views
from cride.users.views import (
    UserLoginAPIView,
    UserSingUpAPIView,
    )


urlpatterns = [
    path ('users/singup/', UserSingUpAPIView.as_view(), name='signup'),
    # esta url es para hacer el signup de usuarios
    path ('users/login/', UserLoginAPIView.as_view(), name='login'),
    # url para hacer login de usuarios
    
]

# el name='login sirve para cuando se haga el reverse quede como 'users:login'
