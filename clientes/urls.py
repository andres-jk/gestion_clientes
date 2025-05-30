# clientes/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # Página de inicio
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('clientes/editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),
]