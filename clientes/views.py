# clientes/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required # Para proteger las vistas

# Vista para listar clientes (requiere login)
@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/lista_clientes.html', {'clientes': clientes})

# Vista para agregar un nuevo cliente (requiere login)
@login_required
def agregar_cliente(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente agregado exitosamente!')
            return redirect('lista_clientes')
    else:
        form = CustomUserCreationForm()
    return render(request, 'clientes/form_cliente.html', {'form': form, 'titulo': 'Agregar Cliente'})

# Vista para editar un cliente existente (requiere login)
@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado exitosamente!')
            return redirect('lista_clientes')
    else:
        form = CustomUserCreationForm(instance=cliente)
    return render(request, 'clientes/form_cliente.html', {'form': form, 'titulo': 'Editar Cliente'})

# Vista para eliminar un cliente (requiere login)
@login_required
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado exitosamente!')
        return redirect('lista_clientes')
    # Si se accede por GET, renderizar una página de confirmación
    return render(request, 'clientes/confirmar_eliminar.html', {'cliente': cliente})

# Vista para la página de inicio (puede ser pública o requerir login)
@login_required # <--- Asegúrate de que esta línea esté aquí
def index(request):
    return render(request, 'clientes/index.html')
