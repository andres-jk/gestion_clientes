# Archivo de configuración principal del proyecto Django.

import os
from pathlib import Path

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta para producción (no compartir)
SECRET_KEY = 'django-insecure-z_i!v-b^h*t&7_b-i17!b@=n#v!l-l(v5w$8t7-&j9e7#0'

# Modo debug (no usar en producción)
DEBUG = True

<<<<<<< HEAD
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '192.168.1.7']
=======
# SECURITY WARNING: keep the secret key used in production secret!
# ¡IMPORTANTE! Para producción, esto DEBE ser una variable de entorno
# Ejemplo en producción: SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
# Para desarrollo, puedes dejar esta, pero ¡CAMBIALA por una fuerte en producción!
SECRET_KEY = 'django-insecure-m#d9$b&2m(2&@w=^2h_1-g-u8r2o(t9x7p&w=g_c&x2l!0d8q1q' # ### CAMBIAR por una CLAVE SECRETA FUERTE Y DIFERENTE ###


# SECURITY WARNING: don't run with debug turned on in production!
# Cuando vayas a desplegar a internet, CAMBIA esto a False
# Cambia esto a False para producción
DEBUG = true

# Si DEBUG es False, DEBES listar los hosts permitidos aquí.
# Para desarrollo local: '127.0.0.1', 'localhost'
# Para producción: 'tudominio.com', 'www.tudominio.com', 'tu_ip_del_servidor'
# gestion_clientes/settings.py

# Cuando despliegues, PythonAnywhere te dará un dominio como 'tucuenta.pythonanywhere.com'
# Añádelo aquí después de crear la app web.
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.pythonanywhere.com'] # Añade el wildcard para facilitar, luego se refina
# Cuando cambies DEBUG a False, deberías añadir tu dominio real aquí.
# Por ejemplo: ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'tudominio.com', 'www.tudominio.com']


# Application definition
>>>>>>> 276fd6a0d95b26d231954188a41a344a63ffc318

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'clientes',         # App principal
    'widget_tweaks',    # Para mejorar formularios en plantillas
]

# Middleware (procesadores de peticiones/respuestas)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gestion_clientes.urls'

# Configuración de plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'clientes' / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'gestion_clientes.wsgi.application'

# Configuración de base de datos (SQLite por defecto)
DATABASES = {
    'default': {
<<<<<<< HEAD
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validadores de contraseñas
=======
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'andresjk$MULTIANDAMIOS', # Esto lo configurarás en PythonAnywhere
        'USER': 'andresjk',       # Esto lo configurarás en PythonAnywhere
        'PASSWORD': 'Aa280425_', # Esto lo configurarás en PythonAnywhere
        'HOST': 'andresjk.mysql.pythonanywhere-services.com',         # Para la DB de PythonAnywhere, este suele ser el host
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    }
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

>>>>>>> 276fd6a0d95b26d231954188a41a344a63ffc318
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

# Internacionalización
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# Archivos estáticos (CSS, JS, imágenes)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'clientes' / 'static',
]

# Tipo de clave primaria por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redirecciones después de login/logout/registro
LOGIN_REDIRECT_URL = '/clientes/redirect/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
LOGIN_URL = '/accounts/login/'

# Configuración de mensajes flash
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'info',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}
<<<<<<< HEAD

# Email backend para desarrollo: muestra los emails en la consola
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
=======
>>>>>>> 276fd6a0d95b26d231954188a41a344a63ffc318
