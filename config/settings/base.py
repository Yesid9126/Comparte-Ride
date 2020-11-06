"""Base settings to build other settings files upon."""
# esta es una libreria que nos permite traer variables booleanas entre otras(Documentacion)
import environ 
#permite utilizar variables de entorno twelve-factor-app para configurar su aplicación Django
# importa una plantilla propia de environ

ROOT_DIR = environ.Path(__file__) - 3 # este es el directorio base
APPS_DIR = ROOT_DIR.path('cride')     # folder cride contenido en el directorio base

env = environ.Env() # env es la instancia de Django environ

# Base
DEBUG = env.bool('DJANGO_DEBUG', False)
# env.bool trae la variable booleana que tiene DJANGO_DEBUG si no tiene  por default false

# Language and timezone
TIME_ZONE = 'America/Mexico_City'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

# DATABASES
DATABASES = {
    'default': env.db('DATABASE_URL'),
}
# creamos un DATABASE_URL y la instancia env.db convierte esta url a los datos de la DB
# como username, password, host

DATABASES['default']['ATOMIC_REQUESTS'] = True
# configuramosque nuestras transacciones sean atomicas e la base de datos

# URLs
ROOT_URLCONF = 'config.urls'
# indicamos donde esta nuestro modulo de urls

# WSGI
WSGI_APPLICATION = 'config.wsgi.application'
# indicamos donde esta el modulo wsgi

# Users & authentication
AUTH_USER_MODEL = 'users.User'
# con esto le indicamos a Django que vamos a usar un modelo de usuario custom

# Apps
DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    # instalamos la aplicacion de rest_framework
    'rest_framework.authtoken',
    # instalamos la aplicacion para crear tokens
    
]
LOCAL_APPS = [
    'cride.users.apps.UsersAppConfig',
    'cride.circles.apps.CirclesAppConfig'
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
# las aplicaciones instaladas son la suma de otras aplicaciones 

# Passwords
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]
# listamos los metodos de cifrado para passwords, en caso de que alguno no este disponible

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
# esto son los validadores de passwords

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Static files
STATIC_ROOT = str(ROOT_DIR('staticfiles'))
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    str(APPS_DIR.path('static')),
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
# seccion de archivos estaticos que no usaremos en esta oportunidad, ya que construiremos una API

# Media
MEDIA_ROOT = str(APPS_DIR('media'))
MEDIA_URL = '/media/'
# le indicamos donde se encuentra la media

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
# aca indicamos como se usan los templates y donde se encuentran ubicados

# Security
SESSION_COOKIE_HTTPONLY = True # esto hace que la sesion se mande por HTTP
CSRF_COOKIE_HTTPONLY = True    # CSRF tambien se envie por HTTP
SECURE_BROWSER_XSS_FILTER = True # que filtre lo de inyeccion
X_FRAME_OPTIONS = 'DENY'   # que no se pueda envever nuestra pagina

# Email
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
# utilizaremos el EMAIL_BACKEND de Django pars enviar correos

# Admin
ADMIN_URL = 'admin/' # esta es la variable que seteamos en produccion puede cambiar
ADMINS = [
    ("""Pablo Trinidad""", 'pablotrinidad@ciencias.unam.mx'),
]
# indicamos los correos de los administradores

MANAGERS = ADMINS

# Celery
INSTALLED_APPS += ['cride.taskapp.celery.CeleryAppConfig']
if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYD_TASK_TIME_LIMIT = 5 * 60
CELERYD_TASK_SOFT_TIME_LIMIT = 60

# para utilizar los renderers debemos importar las siguientes lineas para indicar al render
# como funcionar , los renders reciben cualquier tipo de formato

# Django REST framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        # se analiza si el formato es Json, en caso de que no sea Json salta la siguiente linea
        #'rest_framework.renderers.BrowsableAPIRenderer',
        # este recibe cualquier tipo de formato
    ]
}
