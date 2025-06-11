from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Cliente, Producto, ReciboObra, Devolucion, DevolucionProducto

# Formulario de registro de usuario extendido con campos adicionales
class CustomUserCreationForm(UserCreationForm):
    nombre = forms.CharField(max_length=100, required=True, label="Nombre")
    apellido = forms.CharField(max_length=100, required=True, label="Apellido")
    telefono = forms.CharField(max_length=20, required=False, label="Teléfono")

    class Meta:
        model = User
        fields = ("username", "nombre", "apellido", "telefono", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["nombre"]
        user.last_name = self.cleaned_data["apellido"]
        if commit:
            user.save()
            # Crear el cliente asociado
            Cliente.objects.create(
                user=user,
                apellido=self.cleaned_data["apellido"],
                telefono=self.cleaned_data.get("telefono", ""),
                dni=user.username,  # Puedes cambiar esto si el DNI es diferente
            )
        return user

# Formulario de inicio de sesión personalizado
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Usuario", max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# Formulario para crear/editar productos
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "precio", "precio_semana", "tipo_renta", "stock", "disponible", "imagen"]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_semana': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_renta': forms.Select(attrs={'class': 'form-select'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ReciboObraForm(forms.ModelForm):
    firma = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = ReciboObra
        fields = ["observaciones", "firma"]
        widgets = {
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class DevolucionForm(forms.ModelForm):
    class Meta:
        model = Devolucion
        fields = ["observaciones"]
        widgets = {
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class DevolucionProductoForm(forms.ModelForm):
    class Meta:
        model = DevolucionProducto
        fields = ["producto", "cantidad", "estado"]
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
        }