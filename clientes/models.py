# Modelos principales de la app clientes.

from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    dni = models.CharField(max_length=20, primary_key=True, unique=True)  # Identificación única del cliente
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        nombre = self.user.first_name.strip() if self.user.first_name else ''
        if nombre:
            return f"{nombre} {self.apellido} ({self.dni})"
        return f"{self.apellido} ({self.dni})"

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_semana = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tipo_renta = models.CharField(max_length=20, choices=[('mes', 'Mes'), ('semana', 'Semana')], default='mes')
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

class Pedido(models.Model):
    id = models.CharField(max_length=13, primary_key=True, unique=True, editable=False)  # ID único de 13 dígitos
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    ubicacion = models.CharField(max_length=100)
    metodo_pago = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    direccion_obra = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            import random
            self.id = str(random.randint(10**12, 10**13-1))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='productos', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    tipo_renta = models.CharField(max_length=20, choices=[('mes', 'Mes'), ('semana', 'Semana')], default='mes')
    duracion = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.nombre} x{self.cantidad} ({self.tipo_renta})"

    class Meta:
        verbose_name = 'Producto en Pedido'
        verbose_name_plural = 'Productos en Pedido'

class Remision(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Remisión #{self.id} - Pedido #{self.pedido.id}"

    class Meta:
        verbose_name = 'Remisión'
        verbose_name_plural = 'Remisiones'

class Factura(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    detalle = models.TextField(blank=True)
    estado_pago = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('pagado', 'Pagado')], default='pendiente')

    def __str__(self):
        return f"Factura #{self.id} - Pedido #{self.pedido.id}"

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'

class ReciboObra(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True)
    firma = models.ImageField(upload_to='firmas/', blank=True, null=True)  # Firma virtual

    def __str__(self):
        return f"Recibo de Obra #{self.id} - Pedido #{self.pedido.id}"

    class Meta:
        verbose_name = 'Recibo de Obra'
        verbose_name_plural = 'Recibos de Obra'

class ReciboObraProducto(models.Model):
    recibo_obra = models.ForeignKey(ReciboObra, related_name='productos', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    ESTADO_CHOICES = [
        ('completo', 'Completo'),
        ('con_danios', 'Con daños'),
        ('danado', 'Dañado completamente'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='completo')
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad} ({self.get_estado_display()})"

    class Meta:
        verbose_name = 'Producto en Recibo de Obra'
        verbose_name_plural = 'Productos en Recibo de Obra'

class Devolucion(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Devolución #{self.id} - Pedido #{self.pedido.id}"

    class Meta:
        verbose_name = 'Devolución'
        verbose_name_plural = 'Devoluciones'

class DevolucionProducto(models.Model):
    devolucion = models.ForeignKey(Devolucion, related_name='productos', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    estado = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad} (Devolución #{self.devolucion.id})"

    class Meta:
        verbose_name = 'Producto Devuelto'
        verbose_name_plural = 'Productos Devueltos'

