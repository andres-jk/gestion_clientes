# clientes/models.py

from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True) # <-- Asegúrate de que esta línea exista
    direccion = models.TextField(blank=True, null=True)      # <-- Asegúrate de que esta línea exista
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['apellido', 'nombre']