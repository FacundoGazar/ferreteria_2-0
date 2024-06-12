from django.shortcuts import render, get_object_or_404, redirect
from mis_productos.models import Producto
from .models import PagoServicio
from datetime import datetime
from django.contrib import messages

# Create your views here.
def mis_servicios_view(request):
    return render(request, "gestion_de_servicios/mis_servicios.html")

def listar_solicitudes_view(request):    
    usuario = request.user
    queryset = Producto.objects.filter(cliente=usuario, visible=True)
    context = {
        "lista": queryset
    }
    
    return render(request, "gestion_de_servicios/listar_solicitudes.html", context)

def solicitar_servicio_view(request):    
    return render(request, "gestion_de_servicios/solicitar_servicio.html")

def ver_imagen_view(request, slug):
    producto = Producto.objects.get(slug=slug)
   
    context = {
        'producto': producto,
    }
    return render(request, "gestion_de_servicios/ver_imagen.html", context)

def aprobar_solicitud_view(request):
    return render(request, "gestion_de_servicios/ver_imagen.html")

def pagar_publicacion_view(request, slug):
    producto = Producto.objects.get(slug=slug)
    if request.method == 'POST':
        numero_tarjeta = request.POST.get('numero_tarjeta')
        nombre_dueño = request.POST.get('nombre_dueño')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')
        codigo_seguridad = request.POST.get('codigo_seguridad')
        monto = 5  # Asumiendo que el modelo Servicio tiene un campo 'precio'

        # Validación básica
        if not all([numero_tarjeta, nombre_dueño, fecha_vencimiento, codigo_seguridad]):
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('pagar_publicacion', slug=slug)

        # Convertir fecha_vencimiento a un objeto de fecha si es necesario
        try:
            fecha_vencimiento = datetime.strptime(fecha_vencimiento, '%m/%Y').date()
        except ValueError:
            messages.error(request, "Formato de fecha de vencimiento inválido. Use MM/AAAA.")
            return redirect('pagar_publicacion', slug=slug)

        # Crear una nueva instancia de PagoServicio
        pago = PagoServicio(
            cliente=request.user,
            monto=monto,
            fecha=datetime.now().date()  # Establecer la fecha actual para el pago
        )
        pago.save()

        messages.success(request, "Pago realizado con éxito.")
        return redirect('listar_solicitudes')  # Redirige a una página de éxito o donde desees
    context = {
        'producto': producto,
    }
    return render(request, "gestion_de_servicios/pagar_publicacion.html", context)