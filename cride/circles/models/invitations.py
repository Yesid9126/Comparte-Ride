# """Circle models invitations"""

# # Django
# from django.db import models

# # utilities
# from cride.utils.models import CRideModel

# # Managers
# from cride.circles.managers import InvitationManager

# class Invitation(CRideModel):
#     """Circle invitation.

#     A circle invitation is a random text that acts as
#     a unique code that grants access to a specific circle.
#     This codes are generated  by users that already
#     members of the circle and have a 'remaining_invitations'
#     value greater than 0.
#     """

#     code = models.CharField(max_length=50,unique=True)
# # sabemos quien emitio el codigo de invitacion
#     issued_by = models.ForeignKey(
#         'users.User',
#         on_delete= models.CASCADE,
#         help_text ='Circle member  that is providing the invitation',
#         related_name= 'issued_by',
#     )
# # sabemos quien uso o usara el codigo de invitacion
#     used_by = models.ForeignKey(
#         'users.User',
#         on_delete=models.CASCADE,
#         null = True,
#         help_text = 'User that used the code to enter the circle',
#     )
# # guardamos cual es el circulo
#     circle = models.ForeignKey('circles.Cricle',on_delete=models.CASCADE)

# # definimos si el codigo ah sido usado
#     used= models.BooleanField(default=False)
# # nos indica cuando se uso
#     used_at = models.DateTimeField(blank=True,null= True)

#     # Manager
#     objects = InvitationManager()

#     def __str__(self):
#        """Return code and circle."""
#        return '# {}: {}'.format(self.circle.slug_name,self.code)
        

