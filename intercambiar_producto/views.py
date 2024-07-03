from django.shortcuts import render
from mis_productos.models import Producto
from iniciar_sesion import *
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Intercambio,Venta, ProductoVenta
from catalogo.models import ProductoCatalogo
from .forms import IntercambioForm
from django.db.models import Q
from datetime import datetime, timedelta
from gestion_de_sucursales.models import PerfilEmpleado
from django.utils import timezone
from gestion_de_sucursales.models import Sucursal


@soy_cliente
def intercambiar_listar_mis_productos_view(request, slug_intercambio):
    usuario = request.user
    producto_receptor = Producto.objects.get(slug=slug_intercambio)
    
    intercambios_existentes = Intercambio.objects.filter(
        Q(estado__in=['aceptado', 'realizado']) & (
            Q(producto_solicitante__cliente=usuario) |
            Q(producto_receptor__cliente=usuario)
        ) 
    )
    productos_excluir = set()
    for intercambio in intercambios_existentes:
        if intercambio.producto_solicitante.cliente == usuario:
            productos_excluir.add(intercambio.producto_solicitante.id)
        if intercambio.producto_receptor.cliente == usuario:
            productos_excluir.add(intercambio.producto_receptor.id)
    productos_excluir_list = list(productos_excluir)
    queryset = Producto.objects.filter(cliente=usuario, categoria=producto_receptor.categoria).exclude(id__in=productos_excluir_list)

    context = {
        "lista": queryset,
        "slug_intercambio": slug_intercambio,
    }
    
    return render(request, "intercambiar_producto/intercambiar_listado.html", context)

@soy_cliente
def realizar_intercambio_view(request, slug_intercambio):
    producto_receptor = Producto.objects.get(slug=slug_intercambio)
    hora_inicio_str = producto_receptor.horario_inicio.split(':')[0]
    hora_fin_str = producto_receptor.horario_fin.split(':')[0]
    hora_inicio = int(hora_inicio_str)
    hora_fin = int(hora_fin_str)
    horarios_disponibles = [(hora, str(hora)) for hora in range(hora_inicio, hora_fin + 1)]

    if request.method == 'POST':
        producto_solicitante_id = request.POST.get('producto_solicitante_id')
        producto_solicitante = Producto.objects.get(id=producto_solicitante_id)
        fecha = request.POST.get('fecha')
        if fecha:
            form = IntercambioForm(request.POST, horario_choices=horarios_disponibles, producto_receptor=producto_receptor)
            if form.is_valid():
                producto_solicitante_id = request.POST.get('producto_solicitante_id')
                try:
                    producto_solicitante = Producto.objects.get(id=producto_solicitante_id)
                except Producto.DoesNotExist:
                    messages.error(request, "Producto solicitante no encontrado.")
                    return redirect("intercambiar_producto/intercambiar_listado.html")
                
                intercambio = form.save(commit=False)
                intercambio.producto_solicitante = producto_solicitante
                intercambio.cliente_solicitante = request.user
                intercambio.producto_receptor = producto_receptor
                intercambio.cliente_receptor = producto_receptor.cliente
                intercambio.dia = producto_receptor.dias
                intercambio.estado = 'pendiente'
                intercambio.save()
                messages.success(request, "Solicitud de intercambio enviada con éxito.")
                return redirect('homepage')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)
        else:
            messages.error(request, "La fecha es obligatoria.")
            form = IntercambioForm(request.POST, horario_choices=horarios_disponibles, producto_receptor=producto_receptor)
            return render(request, "intercambiar_producto/realizar_intercambio.html", {'producto_receptor': producto_receptor,
        'horarios_disponibles': horarios_disponibles,'form': form})
    else:
        producto_solicitante_id = request.GET.get('producto_solicitante_id')
        try:
            producto_solicitante = Producto.objects.get(id=producto_solicitante_id)
        except Producto.DoesNotExist:
            messages.error(request, "Producto solicitante no encontrado.")
            return redirect("intercambiar_producto/intercambiar_listado.html")
        
        form = IntercambioForm(horario_choices=horarios_disponibles, producto_receptor=producto_receptor)

    return render(request, 'intercambiar_producto/realizar_intercambio.html', {
        'form': form,
        'producto_solicitante': producto_solicitante,
        'producto_receptor': producto_receptor,
        'horarios_disponibles': horarios_disponibles
    })

@soy_cliente
def ver_intercambios(request):
    usuario_actual = request.user
    solicitudes_enviadas = Intercambio.objects.filter(cliente_solicitante=usuario_actual,estado="pendiente")
    solicitudes_recibidas = Intercambio.objects.filter(cliente_receptor=usuario_actual,estado="pendiente" )

    # Solicitudes aceptadas
    solicitudes_aceptadas = Intercambio.objects.filter(
        Q(cliente_receptor=usuario_actual) | Q(cliente_solicitante=usuario_actual),
        estado="aceptado"
    )

    # Solicitudes realizadas
    solicitudes_realizadas = Intercambio.objects.filter(
        Q(cliente_receptor=usuario_actual) | Q(cliente_solicitante=usuario_actual),
        estado="realizado"
    )

    # Solicitudes canceladas
    solicitudes_canceladas = Intercambio.objects.filter(
        Q(cliente_receptor=usuario_actual) | Q(cliente_solicitante=usuario_actual),
        estado="cancelado"
    )

    # Solicitudes ausentes
    solicitudes_ausentes = Intercambio.objects.filter(
        Q(cliente_receptor=usuario_actual) | Q(cliente_solicitante=usuario_actual),
        estado="ausente"
    )

    # Solicitudes rechazadas
    solicitudes_rechazadas = Intercambio.objects.filter(
        Q(cliente_receptor=usuario_actual) | Q(cliente_solicitante=usuario_actual),
        estado="rechazada"
    )

    if request.method == 'POST':
        intercambio_id = request.POST.get('intercambio_id')
        if intercambio_id:
            try:
                intercambio = Intercambio.objects.get(id=intercambio_id)
                intercambio.delete()
                messages.success(request, "Solicitud cancelada con éxito")
            except Intercambio.DoesNotExist:
                messages.error(request, "La solicitud no existe")
        else:
            messages.error(request, "Algo salió mal")

    context = {
        'solicitudes_enviadas': solicitudes_enviadas,
        'solicitudes_recibidas': solicitudes_recibidas,
        'solicitudes_aceptadas': solicitudes_aceptadas,
        'solicitudes_realizadas': solicitudes_realizadas,
        'solicitudes_canceladas': solicitudes_canceladas,
        'solicitudes_ausentes': solicitudes_ausentes, 
        'solicitudes_rechazadas': solicitudes_rechazadas, 
    }
    return render(request, "intercambiar_producto/ver_intercambios.html", context)

@soy_cliente
def detalle_intercambio(request, solicitud_id):
    solicitud = Intercambio.objects.get(id=solicitud_id)
    
    if request.method == "POST":
        accion = request.POST.get('accion')
        if accion == 'aceptar':
            producto_s = solicitud.producto_solicitante
            producto_r = solicitud.producto_receptor 

            # Rechazar todas las solicitudes pendientes que involucren los mismos productos en cualquier dirección
            solicitudes_a_rechazar = Intercambio.objects.filter(producto_receptor=producto_r).exclude(id=solicitud_id)
            solicitudes_a_rechazar_dos = Intercambio.objects.filter(producto_solicitante=producto_s).exclude(id=solicitud_id)
            
            # Actualiza el estado a 'rechazado' y guarda cada solicitud
            for s in solicitudes_a_rechazar:
                s.estado = 'rechazado'
                s.save()

            # Actualiza el estado a 'rechazado' y guarda cada solicitud
            for s_dos in solicitudes_a_rechazar_dos:
                s_dos.estado = 'rechazado'
                s_dos.save()

            solicitud.estado = 'aceptado'
            solicitud.save()
            messages.success(request, "La solicitud ha sido aceptada.")
        elif accion == 'rechazar':
            solicitud.estado = 'rechazado'
            solicitud.save()
            messages.success(request, "La solicitud ha sido rechazada.")
        elif accion == 'cancelar':
            ahora = timezone.now()  # Hora actual con zona horaria

            # Crear un datetime para el horario del intercambio con la fecha pactada y hora
            horario_intercambio = datetime.combine(solicitud.fecha, datetime.min.time()) + timedelta(hours=solicitud.horario)
            
            # Asegurarse de que horario_intercambio sea consciente de la zona horaria
            horario_intercambio = timezone.make_aware(horario_intercambio, timezone.get_current_timezone())

            diferencia = horario_intercambio - ahora
            
            if diferencia > timedelta(hours=1):
                solicitud.delete()
                messages.success(request, "Solicitud cancelada con éxito")
            else:
                messages.error(request, "No podes cancelar el intercambio con menos de una hora de anticipación. De ausentarse, volveran a ofertarse ambos productos.")
            return redirect('ver_intercambios')
        else:
            messages.error(request, "Algo salió mal")
    
    context = {
        'solicitud': solicitud
    }
    return render(request, 'intercambiar_producto/ver_detalle.html', context)

#Tango

#listar los intercambios por sucursal
@soy_staff
def intercambios_por_sucursal_view(request):
    try:
        empleado = PerfilEmpleado.objects.get(usuario=request.user)
        sucursal = empleado.sucursal
        # Obtener la fecha del formulario si está presente, de lo contrario usar la fecha actual
        fecha_seleccionada = request.GET.get('fecha')
        if fecha_seleccionada:
            fecha_seleccionada = datetime.strptime(fecha_seleccionada, '%Y-%m-%d').date()
        else:
            fecha_seleccionada = datetime.now().date()

        # Filtrar los intercambios por sucursal, fecha y estado
        estados_validos = ['aceptado', 'ausente', 'realizado']
        intercambios = Intercambio.objects.filter(
            producto_receptor__sucursal=sucursal,
            fecha=fecha_seleccionada,
            estado__in=estados_validos
        )

        return render(request, 'intercambiar_producto/intercambios_por_sucursal.html', {
            'sucursal': sucursal,
            'intercambios': intercambios,
            'fecha_seleccionada': fecha_seleccionada
        })
    except PerfilEmpleado.DoesNotExist:
        messages.error(request, "El usuario logueado no tiene un perfil de empleado asociado.")
        return redirect('pagina_de_error')
   
@soy_staff    
def confirmar_intercambio_view(request, intercambio_id):
    print("llego")
    intercambio = get_object_or_404(Intercambio, id=intercambio_id)
    intercambio.estado = 'realizado'
    producto_receptorr = get_object_or_404(Producto, id=intercambio.producto_receptor.id)
    producto_solicitantee = get_object_or_404(Producto, id=intercambio.producto_solicitante.id)
    
    producto_receptorr.visible = False
    producto_solicitantee.visible = False
    
    producto_receptorr.save()
    producto_solicitantee.save()
    intercambio.save()
    messages.success(request, "Intercambio confirmado.")
    return redirect('intercambios_por_sucursal')

@soy_staff
def ausente_intercambio_view(request, intercambio_id):
    intercambio = get_object_or_404(Intercambio, id=intercambio_id)
    intercambio.estado = 'ausente'
    intercambio.save()
    messages.success(request, "Intercambio marcado como ausente.")
    return redirect('intercambios_por_sucursal')


@soy_staff
def marcar_venta_view(request, intercambio_id):
    intercambio = get_object_or_404(Intercambio, id=intercambio_id)
    intercambio.venta_realizada = True
    intercambio.save()
    messages.success(request, "Venta marcada como realizada.")
    return redirect('registrar_venta', intercambio_id=intercambio.id)

@soy_staff
def sin_venta_view(request, intercambio_id):
    intercambio = get_object_or_404(Intercambio, id=intercambio_id)
    intercambio.venta_realizada = False
    intercambio.save()
    messages.success(request, "Intercambio marcado como sin venta.")
    return redirect('intercambios_por_sucursal')

@soy_staff
def registrar_venta_view(request, intercambio_id):
    intercambio = get_object_or_404(Intercambio, id=intercambio_id)
    productos = ProductoCatalogo.objects.all()

    if request.method == 'POST':
        productos_vendidos = request.POST.getlist('producto')
        cantidades_vendidas = request.POST.getlist('cantidad')
        monto_total = request.POST.get('monto_total')
        sucursal_nombre = request.POST.get('sucursal')  # Obtener el nombre de la sucursal seleccionada

        try:
            # Buscar la instancia de Sucursal por nombre
            sucursal = get_object_or_404(Sucursal, nombre=sucursal_nombre)
        except Sucursal.DoesNotExist:
            messages.error(request, f"No se encontró ninguna sucursal con el nombre '{sucursal_nombre}'.")
            return redirect('intercambios_por_sucursal')  # Redirecciona a una página de error adecuada

        # Crear y guardar la venta con la sucursal
        venta = Venta.objects.create(monto_total=monto_total, sucursal=sucursal)
        
        # Asociar productos a la venta
        for producto_id, cantidad in zip(productos_vendidos, cantidades_vendidas):
            producto = get_object_or_404(ProductoCatalogo, id=producto_id)
            ProductoVenta.objects.create(venta=venta, producto=producto, cantidad=cantidad)
        
        messages.success(request, "Venta registrada exitosamente.")
        return redirect('intercambios_por_sucursal')

    sucursales = Sucursal.objects.all()  # Obtener todas las sucursales para el formulario
    return render(request, 'intercambiar_producto/registrar_venta.html', {'productos': productos, 'intercambio': intercambio, 'sucursales': sucursales})