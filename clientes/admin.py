# clientes/admin.py

from django.contrib import admin
from .models import Cliente

# Registra tu modelo aquí
admin.site.register(Cliente)

# Opcional: Personalizar cómo se ve en el admin
# class ClienteAdmin(admin.ModelAdmin):
#     list_display = ('nombre', 'apellido', 'email', 'telefono', 'fecha_registro')
#     search_fields = ('nombre', 'apellido', 'email')
#     list_filter = ('fecha_registro',)
#
# admin.site.register(Cliente, ClienteAdmin)