# administrador para el modelo de circulos

# Django
from django.contrib import admin
# importamos el administrador de django para el modelo de circulos

# Models
from cride.circles.models import Circle
# importamos el modelo que queremos registrar en el admin

@admin.register(Circle)
# registramos el modelo de circulos en el administrador
class CircleAdmin(admin.ModelAdmin):
# creamos el administrador del modelo de circulos el cual hereda de ModelAdmin de django
    list_display =(
        'slug_name',
        'name',
        'is_public',
        'verified',
        'is_limited',
        'member_limit'
        )
    
    search_fields= ('slug_name','name')

    list_filter = ('is_public','verified','is_limited')