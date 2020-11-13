"""Profile Serializer"""

# Django REST Framework
from rest_framework import serializers

# Serializer


# Models
from cride.users.models import Profile

class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile Model Serializer."""

    class Meta:
        """Class Meta."""
        model= Profile
        fields= (
            'picture',
            'biography',
            'rides_taken',
            'rides_offered',
            'reputation',
        )
        # estos datos no se pueden editar
        read_only_fields=(
            'rides_taken',
            'rides_offered',
            'reputation',
        )