""" urls de los usuarios"""

#Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter
# Views 
from .views import users as user_views

router = DefaultRouter()
router.register(r'users', user_views.UserViewSet, basename= 'users')
urlpatterns = [
    path('', include(router.urls))
]




















""" urls antes de usar los viewssets"""
# Views
#from cride.users.views import (
#    UserLoginAPIView,
#    UserSingUpAPIView,
#    AccountVerificationAPIView,
#    )
#urlpatterns = [
#    path ('users/singup/', UserSingUpAPIView.as_view(), name='singup'),
#    # esta url es para hacer el signup de usuarios
#    path ('users/login/', UserLoginAPIView.as_view(), name='login'),
#    # url para hacer login de usuarios
#    path ('users/verify/', AccountVerificationAPIView.as_view(), name= 'verify'),
   # creamos esta url para la verificacion de la cuenta
    
#]

# el name='login sirve para cuando se haga el reverse quede como 'users:login'
