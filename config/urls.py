"""Main URLs module."""

from django.conf import settings # importamos la carpeta de settings a este archivo (urls.py)
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin # traemos el administrador de django



urlpatterns = [
    # Django Admin
    path(settings.ADMIN_URL, admin.site.urls),
    # buscara en el folder settings la variable ADMIN_URL que tiene la url

    path('', include(('cride.circles.urls', 'circles'), namespace = 'circles')),
    # del path original ('') vamos a heredar del archivo de circles.url
    # el namespace es el nombre de la url y nos ayuda a hacer el reverse en django

    path('', include(('cride.users.urls', 'users'), namespace = 'users')),
    # urls para el modulo de usuarios


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# sumamos una url statica donde se encuentran los archivos de la media (imagenes)
