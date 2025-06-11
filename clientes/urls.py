from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.clientes_index_view, name='clientes_index_view'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('clientes/', views.lista_clientes_view, name='lista_clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('catalogos/', views.catalogos_view, name='catalogos'),
    path('catalogo_cliente/', views.catalogo_cliente, name='catalogo_cliente'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('productos_admin/', views.productos_admin_view, name='productos_admin'),
    path('producto/<int:pk>/', views.producto_detail_view, name='producto_detail'),
    path('producto/crear/', views.producto_create_view, name='crear_producto'),
    path('producto/editar/<int:pk>/', views.producto_update_view, name='editar_producto'),
    path('producto/eliminar/<int:pk>/', views.producto_delete_view, name='eliminar_producto'),
    path('carrito/', views.carrito_view, name='carrito'),
    path('carrito/agregar/<int:pk>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/cancelar/', views.cancelar_compra, name='cancelar_compra'),
    path('procesar_pedido/', views.procesar_pedido, name='procesar_pedido'),
    path('pedidos/', views.pedidos_view, name='pedidos'),
    path('remision/<int:pedido_id>/', views.remision_view, name='remision'),
    path('remision_pdf/<int:pedido_id>/', views.remision_pdf, name='remision_pdf'),
    path('enviar_remision_correo/<int:pedido_id>/', views.enviar_remision_correo, name='enviar_remision_correo'),
    path('factura/<int:pedido_id>/', views.factura_view, name='factura'),
    path('factura/cambiar_estado/<int:pedido_id>/', views.cambiar_estado_pago_factura, name='cambiar_estado_pago_factura'),
    path('recibo_obra/<int:pedido_id>/', views.recibo_obra_view, name='recibo_obra'),
    path('recibo_obra_pdf/<int:pedido_id>/', views.recibo_obra_pdf, name='recibo_obra_pdf'),
    path('registrar_devolucion/<int:pedido_id>/', views.registrar_devolucion, name='registrar_devolucion'),
    path('devolucion/<int:pedido_id>/', views.devolucion_view, name='devolucion'),
    path('devolucion_pdf/<int:pedido_id>/', views.devolucion_pdf, name='devolucion_pdf'),
    path('sync_users_to_clientes/', views.sync_users_to_clientes, name='sync_users_to_clientes'),
]

# Las rutas de productos_admin, producto_create, producto_update, producto_delete
# ya apuntan a vistas protegidas por @staff_member_required










