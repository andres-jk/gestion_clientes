from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings # <--- Importa settings
from django.conf.urls.static import static # <--- Importa static
from clientes import views as clientes_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clientes/', include('clientes.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', clientes_views.home_view, name='home'),  # Asegúrate que esta línea apunte a tu vista de inicio
]

# <--- Añade estas líneas SOLO PARA DESARROLLO (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)