# clientes/forms.py

from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'email', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del cliente'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido del cliente'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@dominio.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: +573123456789'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Dirección completa'}),
        }