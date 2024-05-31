from django.shortcuts import render
from mis_productos.models import Producto
from iniciar_sesion import soy_cliente
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Intercambio
from .forms import IntercambioForm

@soy_cliente
def intercambiar_listar_mis_productos_view(request, slug_intercambio):
    usuario = request.user
    producto_receptor = Producto.objects.get(slug=slug_intercambio)
    queryset = Producto.objects.filter(cliente=usuario, categoria=producto_receptor.categoria)

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
        try:
            producto_solicitante = Producto.objects.get(id=producto_solicitante_id)
        except Producto.DoesNotExist:
            messages.error(request, "Producto solicitante no encontrado.")
            return redirect("intercambiar_producto/intercambiar_listado.html")  
        
        form = IntercambioForm(request.POST, horario_choices=horarios_disponibles, producto_receptor=producto_receptor)
        if form.is_valid():
            intercambio = form.save(commit=False)
            intercambio.producto_solicitante = producto_solicitante
            intercambio.cliente_solicitante = request.user
            intercambio.producto_receptor = producto_receptor
            intercambio.cliente_receptor = producto_receptor.cliente
            intercambio.dia = producto_receptor.dias
            print(producto_receptor.dias)
            intercambio.estado = 'pendiente'
            intercambio.save()
            messages.success(request, "Solicitud de intercambio enviada con éxito.")
            return redirect('homepage')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {field}: {error}")
            messages.error(request, "Por favor, verifica el formulario.")
    else:
        producto_solicitante_id = request.GET.get('producto_solicitante_id')
        try:
            producto_solicitante = Producto.objects.get(id=producto_solicitante_id)
        except Producto.DoesNotExist:
            messages.error(request, "Producto solicitante no encontrado.")
            return redirect("intercambiar_producto/intercambiar_listado.html")  
        
        form = IntercambioForm(request.GET, horario_choices=horarios_disponibles, producto_receptor=producto_receptor)

    return render(request, 'intercambiar_producto/realizar_intercambio.html', {
        'form': form,
        'producto_solicitante': producto_solicitante,
        'producto_receptor': producto_receptor
    })
@soy_cliente
def ver_intercambios(request):
    usuario_actual = request.user
    solicitudes_enviadas = Intercambio.objects.filter(cliente_solicitante=usuario_actual)
    solicitudes_recibidas = Intercambio.objects.filter(cliente_receptor=usuario_actual)
    
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
    }
    return render(request, "intercambiar_producto/ver_intercambios.html", context)

@soy_cliente
def ver_intercambios(request):
    usuario_actual = request.user
    solicitudes_enviadas = Intercambio.objects.filter(cliente_solicitante=usuario_actual)
    solicitudes_recibidas = Intercambio.objects.filter(cliente_receptor=usuario_actual)
    
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
    }
    return render(request, "intercambiar_producto/ver_intercambios.html", context)

@soy_cliente
def detalle_intercambio(request, solicitud_id):
    solicitud = Intercambio.objects.get(id=solicitud_id)
    
    if request.method == "POST":
        accion = request.POST.get('accion')
        if accion == 'aceptar':
            solicitud.estado = 'aceptado'
            solicitud.save()
            messages.success(request, "La solicitud ha sido aceptada.")
        elif accion == 'rechazar':
            solicitud.estado = 'rechazado'
            solicitud.save()
            messages.success(request, "La solicitud ha sido rechazada.")
    
    context = {
        'solicitud': solicitud
    }
    return render(request, 'intercambiar_producto/ver_detalle.html', context)



    

