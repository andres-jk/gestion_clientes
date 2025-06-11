from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Cliente, Producto

class ClienteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', first_name='Test')
        self.cliente = Cliente.objects.create(
            dni='123456',
            user=self.user,
            apellido='TestApellido',
            telefono='123456789',
            direccion='Calle Falsa 123'
        )

    def test_cliente_str(self):
        self.assertEqual(str(self.cliente), 'Test TestApellido (123456)')

class ProductoModelTest(TestCase):
    def test_producto_str(self):
        producto = Producto.objects.create(
            nombre='Andamio',
            descripcion='Andamio metálico',
            precio=100000,
            precio_semana=25000,
            tipo_renta='mes',
            stock=10,
            disponible=True
        )
        self.assertEqual(str(producto), 'Andamio')

class ClienteViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.cliente = Cliente.objects.create(
            dni='654321',
            user=self.user,
            apellido='Apellido',
            telefono='987654321',
            direccion='Calle 456'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass')

    def test_lista_clientes_view_forbidden_for_non_staff(self):
        response = self.client.get(reverse('clientes:lista_clientes'))
        self.assertEqual(response.status_code, 403)

    def test_catalogos_view_authenticated(self):
        response = self.client.get(reverse('clientes:catalogos'))
        self.assertEqual(response.status_code, 200)

    def test_register_view_get(self):
        self.client.logout()
        response = self.client.get(reverse('clientes:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_view_post_invalid(self):
        self.client.logout()
        response = self.client.post(reverse('clientes:register'), data={})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Por favor corrige los errores en el formulario.')
