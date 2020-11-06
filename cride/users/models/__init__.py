from .users import User
# al importar el modelo de usuario creqado por nosotros, lo estamos empaquetando
# cuando empaquetamos el modelo de usuario django ya no buscara en el archivo models.py,
# este buscara en el folder models en el archivos __init__.py

# debemos importar el modelo de perfil para que se efectuen las migraciones de user and profile
from .profiles import Profile