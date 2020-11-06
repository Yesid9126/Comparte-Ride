"""serializers de los circulos"""
# crearemos 2 serializer, 1 - para listar los circulos
# 2 - para recibir los datos de entrada y mostrar el circulo
# un serializers sirve para convertir datos de python a JSON y viceversa

# los serializers pueden tomar datos de python y convertirlos a json o datos de json para utilizar en python
# tambien nos ayuda a validar los campos

# Django REST framework
from rest_framework import serializer

class CircleSerializer(serializers.Serializer):