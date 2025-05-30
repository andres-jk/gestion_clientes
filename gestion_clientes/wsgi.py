# gestion_clientes/wsgi.py

"""
WSGI config for gestion_clientes project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys # Asegúrate de que esta línea esté presente

from django.core.wsgi import get_wsgi_application

# Añade estas dos líneas para asegurar que la carpeta del proyecto principal
# (donde está manage.py) esté en el PATH de Python.
# Esto es crucial si tu estructura es ProjectRoot/ProjectRoot/
path = 'C:/Users/andre/mi_entorno_clientes/gestion_clientes' # ### CAMBIA ESTA RUTA POR LA RUTA ABSOLUTA A LA CARPETA QUE CONTIENE 'manage.py' ###
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_clientes.settings')

application = get_wsgi_application()