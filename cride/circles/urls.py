""" urls de los circulos"""

#Django
from django.urls import path

# Views
from cride.circles.views import ListCircles


urlpatterns = [
    path ('circles/', ListCircles)
]
