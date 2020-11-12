"""Circles Serializers"""
""" vamos a crear los serializers de los circulos con el ModelSerializer, esto nos permitira
validar campos, crear, listar y modificar circulos"""
# Django REST framework
from rest_framework import serializers

# Model
from cride.circles.models import Circle

# este serializer lista y crea circulos

class CircleModelSerializer(serializers.ModelSerializer):
    """Circle Model Serializer."""
    member_limit = serializers.IntegerField(
        required = False,
        min_value = 10,
        max_value = 32000,
    )
    is_limited = serializers.BooleanField(default=False)

    class Meta:
        """Meta Class."""
        model = Circle
        # utilizamos los campos definidos en el modelo de circulos
        fields=(
            'name','slug_name','about',
            'picture', 'rides_offered',
            'rides_taken','verified','is_public',
            'is_limited','member_limit'
        )
    # estos son los campos que se mostraran cuando se listen o se creen circulos
# tenemos el serializer y la vista ahora debemos conectarlas
        read_only_fields =(
            'is_public',
            'verified',
            'rides_offered',
            'rides_taken',
        )

#creamos otra validacion que nos indique si is_limit esta presente member_limit tambien
    def validate(self, data):
        """Ensure both members_limit and is_limited are present"""
        members_limit = data.get('members_limit', None)
        is_limited = data.get('is_limited', False)
        # traemos la data por metodo get y no por el diccionario
        # los dos campos deben ser diligenciados, de lo contrario habra una excepcion
        if is_limited ^ bool(members_limit):
            raise serializers.ValidationError('If circle is limited, a member limit must be provied')
        return data