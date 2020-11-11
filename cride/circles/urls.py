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

# View
from cride.circles.views import circles as circle_views

router= DefaultRouter()
router.register(r'circles',circle_views.CircleViewSet , basename='circle')
# DefaultRouter tiene el metodo de register que registra una url con una expresion regular,
# esta expresion regular especifica el path, usa la vista y un basename
# con la url circles podemos utilizar todos los metodos(GET,POST,PUT,PATCH,DELETE)

urlpatterns = [
    path('', include(router.urls))
]

