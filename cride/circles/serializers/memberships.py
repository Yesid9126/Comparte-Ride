"""Memberships Serializer"""

# Django REST Framework
from rest_framework import serializers

# Models
from cride.circles.models import Membership

# Serializers
from cride.users.serializers import UserModelSerializer


class MembershipModelSerializer(serializers.ModelSerializer):
    """Member model serializer"""

    joined_at = serializers.DateTimeField(source='created',read_only=True)
    user = UserModelSerializer(read_only=True)
# este usuario tendra las propiedades del usemodelserializer, que a su vez tiene asignado

    invited_by = serializers.StringRelatedField()
# vamos a traer el username de la persona que envio la invitacion(el username ya tiene representacion en string) para esto vamos a usar
# un serializer relationship ( por default se usa el pkrelated field, por eso cuando
# se hacia una consulta devolvia el id de usuario y circulo mas no los slug_name o user
# el perfil de usuario
    class Meta:
        """Meta class."""
        model = Membership
        fields=(
            'user',
            'is_admin',
            'is_activate',
            'used_invitations','remaining_invitations',
            'invited_by',
            'rides_taken','rides_offered',
            # queremos usar  la fecha de creacion pero con el nombre de otro campo
            # entonces haremos lo siguiente
            'joined_at'
        )
        read_only_fields=(
            'user',
            'used_invitations',
            'invited_by',
            'rides_taken',
            'rides_offered',
        )
# estamos trayendo los miembros al circulo y es importante que por cada miembro nos traiga los
# datos del perfil, como la foto y demas informacion 
        