"""Development settings."""
# este archivo es una herencia de base

from .base import *  # NOQA= es un estandar  indica que no tiene aseguramiento de calidad,
# se puede usar para ignorar advertencias de verificacion automatica de codigo
from .base import env # este archivo hereda de base.py

# Base
DEBUG = True

# Security
SECRET_KEY = env('DJANGO_SECRET_KEY', default='PB3aGvTmCkzaLGRAxDc3aMayKTPTDd5usT8gw4pCmKOk5AlJjh12pTrnNgQyOHCH')
# trae la llave de django de una variable de entorno, si no tiene entonces le asigan default
ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
]
# estos son los unicos host que esta permitidos dentro del desarrollo

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}
# el backend de cache que utilizaremos es el de memoria

# Templates
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # NOQA
# los templates estan en modo debug

# Email
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
# el email de backend sera el mismo e indica el puerto por el que sale

# django-extensions
INSTALLED_APPS += ['django_extensions']  # noqa F405
# instalamos django-extensions que nos permite extender las capacidades de django

# Celery
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
