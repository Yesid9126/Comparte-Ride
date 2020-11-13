"""Cricles urls"""
#Django
#from django.urls import path
# Views
#from cride.circles.views import ListCircles
#urlpatterns = [
#    path ('circles/', ListCircles)
#
""" vamos a conectar las vistas de los circulos con los serializers
esto lo haremos con la funcionalidad de route"""

# Django
from django.urls import include, path

# Django REST framework
from rest_framework.routers import DefaultRouter
# los routers reciben y saber trabajar con viewsets y genera las urls que se necesitan para
# listar, crear actualizar circulos

# Views
from cride.circles.views import circles as circle_views
from .views import memberships as membership_views


router= DefaultRouter()
router.register(r'circles',circle_views.CircleViewSet , basename='circle')
# DefaultRouter tiene el metodo de register que registra una url con una expresion regular,
# esta expresion regular especifica el path, usa la vista y un basename
# con la url circles podemos utilizar todos los metodos(GET,POST,PUT,PATCH,DELETE)
router.register(r'circles/(?P<slug_name>[a-zA-Z0-9_-]+)/members',
                membership_views.MembershipViewSet, 
                basename='membership',
)
# esta url es anidada prjmero estara en circles, luego traera el slug_name del circulo
# luego de esto traera los miembros que es donde empezaremos a trabajar
urlpatterns = [
    path('', include(router.urls))
]

