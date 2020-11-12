"""Membershiop Model."""

# Django
from django.db import models

#Utilities
from cride.utils.models import CRideModel

class Membership(CRideModel):
    """Membership model.
    
    A membership is the table thats holds the relationship betweend
    a user and circle.
    """

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    circle = models.ForeignKey('circles.Circle', on_delete=models.CASCADE)

    is_admin= models.BooleanField(
        'circle admin',
        default = False,
        help_text='Circle admins can update the circles data and manage its members'
    )

    #Invitations
    used_invitations =models.PositiveSmallIntegerField(default=0)
    remaining_invitations = models.PositiveIntegerField(default=0)
    invited_by= models.ForeignKey(
        'users.User',
        null=True, 
        on_delete=models.SET_NULL,
        related_name='invited_by',
# cuando se tienen dos campos que son llave foranea en la DB que referencian al mismo modelo
# se debe definir el related_name
    )
    #statics
    rides_offered = models.PositiveIntegerField(default=0)
    rides_taken = models.PositiveIntegerField(default=0)

    #Status
    is_activate = models.BooleanField(
        'active status',
        default=False,
        help_text='only active users are allowed to interactive in the circle'
    )
# validamos si el miembro dejo de ser parte del circulo

    def __str__(self):
        """Return username and circle."""
        return '@ {} at # {}'.format(
            self.user.username,
            self.circle.slug_name,
        )
        # indicamos el username perteneciente al circulo


