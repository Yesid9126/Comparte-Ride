# aca utilizremos la herencia de modelos y las diferentes maneras de ejecutar.
# utilizaremos el metodo de clase abstracta.
# esta clase nos permitira ver cuando se creo, modifico o elimino un objeto de la DB
# hay dos maneras de crear modelos:1-clase abstracta , 2- modelo proxy
# se diferencian por como tratan los datos en la DB
# las clases abstractas permiten extender las funcionalidades de un modelo

# Django
from django.db import models

# todos los modelos de cride heredaran de este modelo

class CRideModel(models.Model):
    """model base de cride, claee abstracat para herencia de modelos.
    todos nuestros modelos adicionales heredaran de esta clase abstracta
    """
    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        # nos guarda automaticamente la fecha en el momento en el que modelo se crea
        help_text= 'Date time on wich the object was created'
    )

    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        # cada que el modelo llama el metodo save() guardara la fecha.
        help_text= 'Date time on wich the object was last modified'
    )
    
    # crearemos la clase meta que esta incluida en la clase abastracta
    class Meta():
        abstract = True
        # este campo indicarle a la DB que
        get_latest_by = 'created'
        # este campo esta disponible en la clase meta y trae el ultimo dato que fue creado
        ordering = ['-created', '-modified']
        # este campo recibe una tupla de parametros y los obtiene ordenadamente.
        # el ultimo objeto creado sera el primero(-created),(-modified) en caso de que se cree a la misma hora y minuto
    # esta clase meta tambien tiene mas opciones, verificar modelMetaOption, documentacion

# veremos que pasa cuando se crea una clase y se hereda de una clase abstracta

#class Student(CRideModel):
#    name = models.Charfield()
# si queremos añadir opciones a la clase META de la clase abstracta lo hariamos asi:
#    class Meta(CRideModel.META):
#        db_table = 'Student_role' este atributo colocal el nombre que se desea en la DB
## NOTA= cuando una clase no abstracta hereda de una abstracta Django cambia abstract=False

# VALIDAREMOS UN PROXY MODEL, este no actua sobre nuestro proyecto, solo es de practica

#class Person (models.Model):
#    first_name=models.Charfield()
#    last_name = models.ChaField()

#class MyPerson(Person): esta persona no añadiria campos nuevos a la DB 
#    class Meta:
#        proxy = True  este campo le indica a Django que no cree una tabla en la DB
#    def say_hi (name):
#        pass

#MyPerson.objects.all() estariamos llamando al manager del person original

# ricardo = MyPerson.objects.get(pk=1)
# ricardo.say_hi ('pablo') 
# esto traeria el objeto que se encuentra en ricardo y traeria el valor de la funcion say_hi
# esto permite que una persona sin ser una DB agregue esta funcionalidad extra

# rulo = Person.objects.get(pk=2)
# rulo.say_hi('pablo')
# esto no existiria por que estamos buscando en la DB y rulo no existe


