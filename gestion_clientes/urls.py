# gestion_clientes/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView # ¡Necesitas importar esto!

urlpatterns = [
    # Redirige la ruta raíz '/' a '/clientes/'
    path('', RedirectView.as_view(url='clientes/', permanent=True)), # ¡Añade esta línea!

    path('admin/', admin.site.urls),
    path('clientes/', include('clientes.urls')),

    # URLs para el sistema de autenticación de Django
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]