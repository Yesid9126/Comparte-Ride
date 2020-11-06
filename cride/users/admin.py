"""modelo de usuario administrador"""

# Django
from django.contrib import admin # importamos el administrador de django

from django.contrib.auth.admin import UserAdmin
# importamos el usuario de administracion que trae por default django y podemos agregar campos

# Modelos
from cride.users.models import User, Profile

# debemos crear y registrar la clase UserAdmin

class CustomUserAdmin(UserAdmin):

    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_client')
    # estos campos se definieron en los modelos
    # is_staff no esta definido pero hereda de la clase abstracta de user
    list_filter = ('is_client','is_staff','created','modified')

# debemos crear y registrar el profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = ('user','reputation', 'rides_taken','rides_offered')
    serach_fields = ('user__username', 'user__email', 'user__first_name','user__last_name')
    list_filter = ('reputation',)

admin.site.register (User, CustomUserAdmin)
# registramos en el admin la clase CustomUserAdmin