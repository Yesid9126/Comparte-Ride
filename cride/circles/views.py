""" vista de circulos"""

from rest_framework.decorators import api_view
# importamos este decorador hace que el objeto request sea de django rest framework
# otro decorador podria ser @throttle_class= hable de cuantos request por frame de tiempo se pueden hacer a esa peticion

from django.http import JsonResponse
# un jsonresponse recibe diccionarios vacios etc mirar documentacion request and response objects

from cride.circles.models import Circle


def ListCircles(request):
    circles = Circle.objects.all() # query para traer todos los circulos de la DB
# esta sentencia nos traera todos os circulos que hayan en la base de datos
# pero solo ira a consultar a la base de datos en el momento que se necesite el valor de circles
    public = circles.filter(is_public=True)
    # realizamos otro query para saber cuales son publicos
    data =[]
    # creamos un diccionario vacio que llenaremos con el listado de los circulos
    for circle in public:
        print(circle)

    return JsonResponse('hola', safe= False)