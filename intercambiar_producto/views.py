from django.shortcuts import render
from mis_productos.models import Producto
from iniciar_sesion import soy_cliente
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Intercambio
from .forms import IntercambioForm
from django.db.models import Q
from datetime import datetime, timedelta
from gestion_de_sucursales.models import PerfilEmpleado
from django.utils import timezone


@soy_cliente
def intercambiar_listar_mis_productos_view(request, slug_intercambio):
    usuario = request.user
    producto_receptor = Producto.objects.get(slug=slug_intercambio)
    
    intercambios_existentes = Intercambio.objects.filter(
        Q(estado__in=['aceptado']) & (
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
    solicitudes_aceptadas = Intercambio.objects.filter(cliente_receptor=usuario_actual,estado="aceptado")
    solicitudes_realizadas = Intercambio.objects.filter(cliente_receptor=usuario_actual,estado="realizado")
    solicitudes_canceladas = Intercambio.objects.filter(cliente_receptor=usuario_actual,estado="cancelado")
    
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
            # Depuración: imprime los productos involucrados
            print(f"Producto solicitante: {producto_s}")
            print(f"Producto receptor: {producto_r}")

            # Rechazar todas las solicitudes pendientes que involucren los mismos productos en cualquier dirección
            pending_solicitudes = Intercambio.objects.filter(
                estado='pendiente',
                producto_solicitante__in=[producto_s, producto_r],
                producto_receptor__in=[producto_s, producto_r]
            ).exclude(id=solicitud_id)
            
            # Depuración: imprime la cantidad de solicitudes encontradas
            print(f"Solicitudes pendientes: {pending_solicitudes.count()}")

            # Depuración: imprime los estados antes de la actualización
            for s in pending_solicitudes:
                print(f"Solicitud antes de actualizar: {s.id} - Estado: {s.estado}")

            # Actualiza el estado a 'rechazado' y guarda cada solicitud
            for s in pending_solicitudes:
                s.estado = 'rechazado'
                s.save()
            
            # Depuración: imprime los estados después de la actualización
            for s in pending_solicitudes:
                print(f"Solicitud después de actualizar: {s.id} - Estado: {s.estado}")

            solicitud.estado = 'aceptado'
            solicitud.save()
            messages.success(request, "La solicitud ha sido aceptada.")
        elif accion == 'rechazar':
            solicitud.estado = 'rechazado'
            solicitud.save()
            messages.success(request, "La solicitud ha sido rechazada.")
        elif accion == 'cancelar':
            try:
                intercambio_id = request.POST.get('intercambio_id')
                intercambio = Intercambio.objects.get(id=intercambio_id)
                if intercambio_id:
            
                
                # Depuración: Verifica que los campos están presentes
                    print(f"Fecha del intercambio: {intercambio.fecha}")
                    print(f"Horario del intercambio: {intercambio.horario}")

                    try:
                        intercambio_datetime = datetime.combine(intercambio.fecha, datetime.strptime(intercambio.horario, '%H:%M').time())
                        print(f"Fecha y hora del intercambio: {intercambio_datetime}")
                    except Exception as e:
                        print(f"Error al combinar fecha y hora: {e}")
                        messages.error(request, f"Error al combinar fecha y hora: {e}")
                        return redirect('intercambiar_producto/ver_intercambios.html')

                    ahora = datetime.now()
                    print(f"Hora actual: {ahora}")
                
                    try:
                        hora_limite = intercambio_datetime - timedelta(hours=1)
                        print(f"Hora límite: {hora_limite}")
                    except Exception as e:
                        print(f"Error al calcular hora límite: {e}")
                        messages.error(request, f"Error al calcular hora límite: {e}")
                        return redirect('intercambiar_producto/ver_intercambios.html')

                    if ahora >= hora_limite:
                        messages.error(request, "No puedes cancelar la solicitud dentro de la próxima hora antes del intercambio. Horario límite.")
                    else:
                        intercambio.delete()
                        messages.success(request, "Solicitud cancelada con éxito")
            except Intercambio.DoesNotExist:
                messages.error(request, "La solicitud no existe")
            except Exception as e:
                print(f"Error inesperado: {e}")
                messages.error(request, f"Error inesperado: {e}")
        else:
            messages.error(request, "Algo salió mal")
    
    context = {
        'solicitud': solicitud
    }
    return render(request, 'intercambiar_producto/ver_detalle.html', context)

#Tango

#listar los intercambios por sucursal
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
   
    
def confirmar_intercambio_view(request, intercambio_id):
    print("llego")
    intercambio = get_object_or_404(Intercambio, id=intercambio_id)
    intercambio.estado = 'realizado'
    intercambio.save()
    messages.success(request, "Intercambio confirmado.")
    return redirect('intercambios_por_sucursal')

def ausente_intercambio_view(request, intercambio_id):
    intercambio = get_object_or_404(Intercambio, id=intercambio_id)
    intercambio.estado = 'ausente'
    intercambio.save()
    messages.success(request, "Intercambio marcado como ausente.")
    return redirect('intercambios_por_sucursal')