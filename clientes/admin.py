# Archivo de configuración del panel de administración de Django para la app clientes.

from django.contrib import admin
from .models import Cliente, Producto, Pedido, PedidoProducto, Remision, Factura, ReciboObra, Devolucion, DevolucionProducto

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('dni', 'user', 'apellido', 'telefono', 'direccion')
    search_fields = ('dni', 'user__username', 'apellido', 'telefono')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'precio_semana', 'tipo_renta', 'stock', 'disponible')
    search_fields = ('nombre',)
    list_filter = ('disponible', 'tipo_renta')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha', 'ubicacion', 'metodo_pago', 'total', 'direccion_obra')
    search_fields = ('usuario__username', 'ubicacion', 'direccion_obra')
    list_filter = ('fecha', 'ubicacion', 'metodo_pago')

@admin.register(PedidoProducto)
class PedidoProductoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'nombre', 'cantidad', 'tipo_renta', 'duracion')
    search_fields = ('nombre',)

@admin.register(Remision)
class RemisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'fecha', 'observaciones')
    search_fields = ('pedido__id',)

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'fecha', 'total', 'estado_pago')
    search_fields = ('pedido__id',)
    list_filter = ('estado_pago',)

@admin.register(ReciboObra)
class ReciboObraAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'fecha', 'observaciones')
    search_fields = ('pedido__id',)

@admin.register(Devolucion)
class DevolucionAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'fecha', 'observaciones')
    search_fields = ('pedido__id',)

@admin.register(DevolucionProducto)
class DevolucionProductoAdmin(admin.ModelAdmin):
    list_display = ('devolucion', 'producto', 'cantidad', 'estado')
    search_fields = ('producto__nombre',)

# Ejemplo de personalización del admin (comentado):
# class ClienteAdmin(admin.ModelAdmin):
#     list_display = ('nombre', 'apellido', 'email', 'telefono', 'fecha_registro')
#     search_fields = ('nombre', 'apellido', 'email')
#     list_filter = ('fecha_registro',)
# admin.site.register(Cliente, ClienteAdmin)