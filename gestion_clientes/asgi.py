# gestion_clientes/asgi.py

import os
import sys # Añade esta línea si la necesitas para el path, como en wsgi.py

from django.core.asgi import get_asgi_application

# Similar al wsgi.py, si tienes problemas de ModuleNotFoundError,
# añade la ruta del proyecto aquí también.
# path = 'C:/Users/andre/mi_entorno_clientes/gestion_clientes' # CAMBIA ESTA RUTA POR LA RUTA ABSOLUTA A LA CARPETA QUE CONTIENE 'manage.py'
# if path not in sys.path:
#     sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_clientes.settings')

application = get_asgi_application()