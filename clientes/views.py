from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test # <--- Importa user_passes_test
from .models import Cliente, Producto, Pedido, PedidoProducto, Remision, Factura, ReciboObra, Devolucion, DevolucionProducto
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.db import IntegrityError
from django.contrib import messages
from .forms import ProductoForm, ReciboObraForm, DevolucionForm, DevolucionProductoForm
from django.views.decorators.http import require_POST, require_GET
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from django.utils import timezone
from django.template.loader import get_template
from django.http import FileResponse
import io
from xhtml2pdf import pisa
from django.forms import modelformset_factory

# PDF

def is_employee(user):
    return user.groups.filter(name='Empleados').exists()

def home_view(request):
    is_user_employee = False
    if request.user.is_authenticated:
        is_user_employee = is_employee(request.user)

    # Cambia 'clientes/home.html' por 'clientes/index.html'
    return render(request, 'clientes/index.html', {'is_user_employee': is_user_employee})

# NUEVA VISTA para la página de inicio de la app 'clientes'
def clientes_index_view(request):
    return render(request, 'clientes/index.html') # Puedes crear una plantilla clientes/index.html

# Vista para el registro de usuarios
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        direccion_obra = request.POST.get('direccion_obra', '')
        if form.is_valid():
            try:
                user = form.save(commit=True)
                # Guarda la dirección de la obra en el modelo Cliente si lo deseas
                cliente = Cliente.objects.get(user=user)
                cliente.direccion = direccion_obra
                cliente.save()
                login(request, user)
                return redirect('clientes:clientes_index_view')
            except IntegrityError:
                messages.error(request, "Este usuario ya tiene un cliente asociado.")
                if user.pk:
                    user.delete()
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def lista_clientes_view(request):
    # Solo empleados o superusuarios pueden ver la lista de clientes
    if not (request.user.is_superuser or request.user.groups.filter(name='Empleados').exists()):
        return HttpResponse("No tienes permiso para ver esta página.", status=403)
    # Eliminar cliente con dni='dn1' si existe
    Cliente.objects.filter(dni='dn1').delete()
    buscar_id = request.GET.get('buscar_id')
    if buscar_id:
        clientes_list = Cliente.objects.filter(dni__icontains=buscar_id)
    else:
        clientes_list = Cliente.objects.all()
    return render(request, 'clientes/lista_clientes.html', {'clientes': clientes_list})

@login_required
def catalogos_view(request):
    # Cualquier usuario autenticado puede ver productos disponibles
    productos = Producto.objects.filter(disponible=True) # Obtiene solo productos disponibles
    return render(request, 'clientes/catalogos.html', {'productos': productos})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Cambia 'home' por el nombre de tu vista de inicio
    return HttpResponse("Login page")

def logout_view(request):
    return HttpResponse("Logout page")

def crear_cliente(request):
    return HttpResponse("Crear cliente")

def editar_cliente(request, pk):
    return HttpResponse(f"Editar cliente {pk}")

def eliminar_cliente(request, pk):
    return HttpResponse(f"Eliminar cliente {pk}")

def sync_users_to_clientes(request):
    # Solo superusuarios pueden ejecutar esto
    if not request.user.is_superuser:
        return HttpResponse("No autorizado", status=403)
    try:
        empleados_group = Group.objects.get(name='Empleados')
        usuarios = User.objects.exclude(is_superuser=True).exclude(groups=empleados_group)
    except Group.DoesNotExist:
        usuarios = User.objects.exclude(is_superuser=True)
    creados = 0
    procesados = []
    for user in usuarios:
        if not Cliente.objects.filter(email=user.email).exists() and user.email:
            Cliente.objects.create(
                user=user,  # user es el objeto User creado previamente
                apellido="",
                telefono="",
                dni="",
                direccion=""
            )
            creados += 1
            procesados.append(user.username)











    pass    # ...vista solo para clientes autenticados...def catalogo_cliente(request):@login_required    pass    # ...vista solo para admins...def admin_dashboard(request):@staff_member_required    return HttpResponse(f"Clientes creados: {creados}<br>Usuarios procesados: {', '.join(procesados)}")
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

@require_POST
def agregar_al_carrito(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    cantidad = int(request.POST.get('cantidad', 1))
    tipo_renta = request.POST.get('tipo_renta', 'mes')
    duracion = int(request.POST.get('duracion', 1))
    carrito = get_carrito(request)
    pk_str = str(pk)
    # Guardar tipo de renta y duración en el carrito
    if pk_str in carrito:
        carrito[pk_str]['cantidad'] += cantidad
        carrito[pk_str]['duracion'] = duracion
        carrito[pk_str]['tipo_renta'] = tipo_renta
    else:
        carrito[pk_str] = {
            'cantidad': cantidad,
            'tipo_renta': tipo_renta,
            'duracion': duracion,
        }
    # Descontar del inventario SOLO si el modelo Producto tiene el campo 'stock' o 'inventario'
    # Cambia 'stock' por el nombre real del campo en tu modelo
    stock_field = None
    if hasattr(producto, 'stock'):
        stock_field = 'stock'
    elif hasattr(producto, 'inventario'):
        stock_field = 'inventario'
    # Si tienes un campo de stock/inventario, descuéntalo
    if stock_field:
        stock_actual = getattr(producto, stock_field)
        if producto.disponible and stock_actual >= cantidad:
            setattr(producto, stock_field, stock_actual - cantidad)
            if getattr(producto, stock_field) == 0:
                producto.disponible = False
            producto.save()
        else:
            messages.error(request, "No hay suficiente inventario para este producto.")
            return redirect('clientes:catalogos')
    # Si no hay campo de stock, solo guarda el carrito
    save_carrito(request, carrito)
    return redirect('clientes:carrito')

@login_required
def login_redirect_view(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('clientes:admin_dashboard')  # Usa el namespace 'clientes'
    else:
        return redirect('clientes:catalogo_cliente')  # Usa el namespace 'clientes'

@staff_member_required
def admin_dashboard(request):
    # Vista solo para administradores
    # ...tu lógica de dashboard admin...
    return render(request, 'clientes/admin_dashboard.html')

@login_required
def catalogo_cliente(request):
    # Vista solo para clientes autenticados
    # ...tu lógica de catálogo y cotización...
    return render(request, 'clientes/catalogo_cliente.html')

@staff_member_required
def producto_create_view(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('clientes:productos_admin')
    else:
        form = ProductoForm()
    return render(request, 'clientes/producto_form.html', {'form': form, 'accion': 'Añadir'})

@staff_member_required
def producto_update_view(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('clientes:productos_admin')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'clientes/producto_form.html', {'form': form, 'accion': 'Editar'})

@staff_member_required
def producto_delete_view(request, pk):
    # Solo administradores pueden acceder
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('clientes:productos_admin')
    return render(request, 'clientes/producto_confirm_delete.html', {'producto': producto})

@staff_member_required
def productos_admin_view(request):
    # Solo administradores pueden acceder
    productos = Producto.objects.all()
    return render(request, 'clientes/productos_admin.html', {'productos': productos})

@login_required
def producto_detail_view(request, pk):
    producto = get_object_or_404(Producto, pk=pk, disponible=True)
    return render(request, 'clientes/producto_detail.html', {'producto': producto})

def get_carrito(request):
    return request.session.setdefault('carrito', {})

def save_carrito(request, carrito):
    request.session['carrito'] = carrito
    request.session.modified = True

def carrito_view(request):
    carrito = get_carrito(request)
    productos = []
    total = 0
    for pk, item in carrito.items():
        # --- Solución: asegurar formato de item ---
        if isinstance(item, int):
            # Migrar formato antiguo a nuevo formato
            item = {'cantidad': item, 'tipo_renta': 'mes', 'duracion': 1}
        producto = Producto.objects.filter(pk=pk).first()
        if producto:
            cantidad = item.get('cantidad', 1)
            tipo_renta = item.get('tipo_renta', 'mes')
            duracion = item.get('duracion', 1)
            if tipo_renta == 'semana' and producto.precio_semana:
                precio_unitario = producto.precio_semana
            else:
                precio_unitario = producto.precio
            subtotal = precio_unitario * cantidad * duracion
            productos.append({
                'producto': producto,
                'cantidad': cantidad,
                'tipo_renta': tipo_renta,
                'duracion': duracion,
                'precio_unitario': precio_unitario,
                'subtotal': subtotal,
            })
            total += subtotal

    iva_porcentaje = 19
    iva_valor = total * iva_porcentaje / 100
    total_con_iva = total + iva_valor

    ubicacion = request.GET.get('ubicacion')
    envio = None
    if ubicacion == "bogota":
        envio = 15000
    elif ubicacion == "cundinamarca":
        envio = 30000
    elif ubicacion == "otra":
        envio = 50000

    total_envio = total_con_iva + envio if envio is not None else None

    return render(request, 'clientes/carrito.html', {
        'carrito_items': productos,
        'total': total,
        'iva_porcentaje': iva_porcentaje,
        'iva_valor': iva_valor,
        'total_con_iva': total_con_iva,
        'envio': envio,
        'total_envio': total_envio,
    })

@csrf_exempt
def procesar_pedido(request):
    if request.method == "POST":
        carrito = get_carrito(request)
        productos = []
        total = 0
        for pk, item in carrito.items():
            if isinstance(item, int):
                item = {'cantidad': item, 'tipo_renta': 'mes', 'duracion': 1}
            producto_obj = Producto.objects.get(pk=pk)
            cantidad = item.get('cantidad', 1)
            tipo_renta = item.get('tipo_renta', 'mes')
            duracion = item.get('duracion', 1)
            if tipo_renta == 'semana' and producto_obj.precio_semana:
                precio_unitario = producto_obj.precio_semana
            else:
                precio_unitario = producto_obj.precio
            subtotal = precio_unitario * cantidad * duracion
            productos.append({
                'nombre': producto_obj.nombre,
                'cantidad': cantidad,
                'tipo_renta': tipo_renta,
                'duracion': duracion,  # <-- Guarda la duración aquí
            })
            total += subtotal

        ubicacion = request.POST.get('ubicacion')
        metodo_pago = request.POST.get('metodo_pago')
        direccion_obra = request.POST.get('direccion_obra')
        envio = 0
        if ubicacion == "bogota":
            envio = 15000
        elif ubicacion == "cundinamarca":
            envio = 30000
        elif ubicacion == "otra":
            envio = 50000
        iva_porcentaje = 19
        iva_valor = total * iva_porcentaje / 100
        total_con_iva = total + iva_valor
        total_envio = total_con_iva + envio

        pedido = Pedido.objects.create(
            usuario=request.user,
            ubicacion=ubicacion,
            metodo_pago=metodo_pago,
            total=total_envio,
            direccion_obra=direccion_obra,
        )
        for prod in productos:
            PedidoProducto.objects.create(
                pedido=pedido,
                nombre=prod['nombre'],
                cantidad=prod['cantidad'],
                # Guarda duración y tipo_renta si existen en el modelo
                duracion=prod['duracion'],
                tipo_renta=prod['tipo_renta'],
            )
        from .models import Remision
        Remision.objects.get_or_create(pedido=pedido)
        save_carrito(request, {})
        return render(request, 'clientes/pedido_exitoso.html', {
            'total_envio': total_envio,
            'metodo_pago': metodo_pago,
            'ubicacion': ubicacion,
            'pedido': pedido,
        })
    return redirect('clientes:carrito')

from django.contrib.auth.decorators import user_passes_test, login_required

def es_admin_o_empleado(user):
    return user.is_superuser or user.groups.filter(name='Empleados').exists()

@login_required
@user_passes_test(es_admin_o_empleado)
def pedidos_view(request):
    pedidos = Pedido.objects.select_related('usuario').prefetch_related('productos').order_by('-fecha')
    pedidos_info = []
    for pedido in pedidos:
        productos = []
        for prod in pedido.productos.all():
            tipo_renta = getattr(prod, 'tipo_renta', 'mes')
            duracion = getattr(prod, 'duracion', 1)
            productos.append({
                'nombre': prod.nombre,
                'cantidad': prod.cantidad,
                'tipo_renta': tipo_renta,
                'duracion': duracion,
            })
        pedidos_info.append({
            'pedido': pedido,
            'productos': productos,
            'direccion_obra': getattr(pedido, 'direccion_obra', ''),
        })
    return render(request, 'clientes/pedidos.html', {'pedidos_info': pedidos_info})

def eliminar_producto(request, pk):
    # Vista temporal para evitar error
    return HttpResponse(f"Vista para eliminar producto {pk} (pendiente de implementar)")

@require_GET
@login_required
def cancelar_compra(request):
    carrito = get_carrito(request)
    for pk, item in carrito.items():
        # Asegura formato de item
        if isinstance(item, int):
            item = {'cantidad': item, 'tipo_renta': 'mes', 'duracion': 1}
        producto = Producto.objects.filter(pk=pk).first()
        cantidad = item.get('cantidad', 1)
        # Devuelve el stock/inventario si el modelo lo tiene
        if producto:
            if hasattr(producto, 'stock'):
                producto.stock += cantidad
                producto.disponible = True
                producto.save()
            elif hasattr(producto, 'inventario'):
                producto.inventario += cantidad
                producto.disponible = True
                producto.save()
    save_carrito(request, {})
    messages.success(request, "La compra ha sido cancelada y el inventario restaurado.")
    return redirect('clientes:catalogos')

@login_required
def remision_view(request, pedido_id):
    remision, created = Remision.objects.get_or_create(pedido_id=pedido_id)
    productos = []
    for prod in remision.pedido.productos.all():
        tipo_renta = getattr(prod, 'tipo_renta', 'mes')
        duracion = getattr(prod, 'duracion', 1)
        productos.append({
            'nombre': prod.nombre,
            'cantidad': prod.cantidad,
            'tipo_renta': tipo_renta,
            'duracion': duracion,
        })
    # Generar factura si no existe
    factura, factura_created = Factura.objects.get_or_create(
        pedido=remision.pedido,
        defaults={
            'total': remision.pedido.total,
            'detalle': '',
        }
    )
    return render(request, 'clientes/remision.html', {
        'remision': remision,
        'productos_remision': productos,
        'direccion_obra': remision.pedido.direccion_obra if hasattr(remision.pedido, 'direccion_obra') else '',
        'factura': factura,
    })

@login_required
def factura_view(request, pedido_id):
    factura = Factura.objects.select_related('pedido').get(pedido_id=pedido_id)
    productos = []
    for prod in factura.pedido.productos.all():
        productos.append({
            'nombre': prod.nombre,
            'cantidad': prod.cantidad,
            'tipo_renta': prod.tipo_renta,
            'duracion': prod.duracion,
        })
    # Enviar la factura por correo al usuario si se solicita por GET param ?enviar=1
    if request.GET.get('enviar') == '1':
        subject = f"Factura #{factura.id} - Multiandamios"
        to_email = factura.pedido.usuario.email
        html_message = render_to_string('clientes/factura_email.html', {
            'factura': factura,
            'productos_factura': productos,
            'direccion_obra': factura.pedido.direccion_obra if hasattr(factura.pedido, 'direccion_obra') else '',
        })
        send_mail(
            subject,
            '',  # plain text body (opcional)
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            html_message=html_message,
            fail_silently=False,
        )
        messages.success(request, f"La factura ha sido enviada al correo {to_email}.")
    return render(request, 'clientes/factura.html', {
        'factura': factura,
        'productos_factura': productos,
        'direccion_obra': factura.pedido.direccion_obra if hasattr(factura.pedido, 'direccion_obra') else '',
    })

@staff_member_required
def cambiar_estado_pago_factura(request, pedido_id):
    factura = Factura.objects.get(pedido_id=pedido_id)
    if request.method == "POST":
        nuevo_estado = request.POST.get('estado_pago')
        if nuevo_estado in ['pendiente', 'pagado']:
            factura.estado_pago = nuevo_estado
            factura.save()
            messages.success(request, "Estado de pago actualizado correctamente.")
    return redirect('clientes:factura', pedido_id=pedido_id)

@login_required
def remision_pdf(request, pedido_id):
    remision = get_object_or_404(Remision, pedido_id=pedido_id)
    productos = remision.pedido.productos.all()
    template = get_template('clientes/remision.html')
    context = {
        'remision': remision,
        'productos_remision': productos,
        'direccion_obra': remision.pedido.direccion_obra if hasattr(remision.pedido, 'direccion_obra') else '',
    }
    html = template.render(context)
    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=result)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    result.seek(0)
    return FileResponse(result, as_attachment=True, filename=f'Remision_{remision.id}.pdf')

@login_required
def enviar_remision_correo(request, pedido_id):
    remision = get_object_or_404(Remision, pedido_id=pedido_id)
    productos = []
    for prod in remision.pedido.productos.all():
        tipo_renta = getattr(prod, 'tipo_renta', 'mes')
        duracion = getattr(prod, 'duracion', 1)
        productos.append({
            'nombre': prod.nombre,
            'cantidad': prod.cantidad,
            'tipo_renta': tipo_renta,
            'duracion': duracion,
        })
    to_email = remision.pedido.usuario.email
    subject = f"Remisión #{remision.id} - Multiandamios"
    html_message = render_to_string('clientes/remision.html', {
        'remision': remision,
        'productos_remision': productos,
        'direccion_obra': remision.pedido.direccion_obra if hasattr(remision.pedido, 'direccion_obra') else '',
    })
    send_mail(
        subject,
        '',  # plain text body opcional
        settings.DEFAULT_FROM_EMAIL,
        [to_email],
        html_message=html_message,
        fail_silently=False,
    )
    messages.success(request, f"La remisión ha sido enviada al correo {to_email}.")
    return redirect('clientes:remision', pedido_id=pedido_id)

def recibo_obra_view(request, pedido_id):
    from django.core.exceptions import ObjectDoesNotExist
    import base64
    from django.core.files.base import ContentFile
    try:
        pedido = Pedido.objects.get(id=pedido_id)
    except Pedido.DoesNotExist:
        messages.error(request, f"No existe un pedido con ID {pedido_id}.")
        return render(request, 'clientes/recibo_obra.html', {
            'form': None,
            'pedido': None,
            'recibo': None,
            'pedido_no_existe': True,
            'pedido_id': pedido_id,
        })
    recibo, created = ReciboObra.objects.get_or_create(pedido=pedido)
    if request.method == 'POST':
        form = ReciboObraForm(request.POST, request.FILES, instance=recibo)
        firma_data = request.POST.get('firma')
        if firma_data and firma_data.startswith('data:image'):
            format, imgstr = firma_data.split(';base64,')
            ext = format.split('/')[-1]
            recibo.firma.save(f'firma_{pedido_id}.{ext}', ContentFile(base64.b64decode(imgstr)), save=False)
        if form.is_valid():
            form.save()
            productos_devueltos = []
            for prod in pedido.productos.all():
                estado = request.POST.get(f'estado_producto_{prod.id}', 'completo')
                observaciones = request.POST.get(f'observaciones_producto_{prod.id}', '')
                from .models import ReciboObraProducto, Devolucion, DevolucionProducto, Producto
                # Buscar el producto por nombre, pero tomar el primero si hay duplicados
                producto_obj = Producto.objects.filter(nombre=prod.nombre).first()
                if not producto_obj:
                    continue  # Si no existe, omitir
                robj, _ = ReciboObraProducto.objects.get_or_create(
                    recibo_obra=recibo,
                    producto=producto_obj,
                    defaults={'cantidad': prod.cantidad}
                )
                robj.estado = estado
                robj.observaciones = observaciones
                robj.cantidad = prod.cantidad
                robj.save()
                # Si el producto fue devuelto (dañado o con daños), registrar devolución y actualizar inventario
                if estado in ['danado', 'con_danios']:
                    productos_devueltos.append((producto_obj, prod.cantidad, estado))
            # Registrar devolución si hay productos de