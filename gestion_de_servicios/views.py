from django.shortcuts import render, redirect
from mis_productos.models import Producto
from gestion_de_sucursales.models import Sucursal
from .models import PagoServicio, Servicio, Tarjeta
from datetime import datetime
from django.contrib import messages
from .forms import ServicioForm
from django.core.exceptions import ValidationError
from PIL import Image, ImageChops
from django.core.mail import send_mail
from iniciar_sesion.decoradores import *

# Create your views here.
@soy_cliente
def mis_servicios_view(request):
    return render(request, "gestion_de_servicios/mis_servicios.html")

@soy_cliente
def listar_solicitudes_view(request):    
    usuario = request.user
    queryset = Servicio.objects.filter(cliente=usuario)
    context = {
        "lista": queryset
    }
    
    return render(request, "gestion_de_servicios/listar_solicitudes.html", context)

@soy_cliente
def subir_servicio_view(request):
    sucursales = Sucursal.objects.all()

    if request.method == "POST":
        form = ServicioForm(request.POST, request.FILES)

        imagen = request.FILES.get('imagen')
        if imagen:
            formato_valido, mensaje_error = verificar_formato_imagen(imagen)
            if not formato_valido:
                messages.error(request, mensaje_error)
                return render(request, "gestion_de_servicios/solicitar_servicio.html", {
                    "form": form,
                    "sucursales": sucursales,
                })
        else:
            messages.error(request, "Es obligatorio subir la imagen del flyer del servicio.")
            return render(request, "gestion_de_servicios/solicitar_servicio.html", {
                    "form": form,
                    "sucursales": sucursales,
                })
        
        if form.is_valid():          
            servicio = form.save(commit=False)
            servicio.cliente = request.user
            servicio.save()
            
            if are_images_equal(servicio.id):
                servicio.delete()
                messages.error(request, "¡Este servicio ya fue ofertado en el sitio!")
            else:
                messages.success(request, "¡Se ha solicitado la publicacion del servicio correctamente!")
            return redirect("mis_servicios")
        
    else:
        form = ServicioForm()
        
    return render(request, "gestion_de_servicios/solicitar_servicio.html", {
        "form": form,
        "sucursales": sucursales,
    })

def are_images_equal(servicio_slug):
    servicio = Servicio.objects.get(id=servicio_slug)
    comparativas = Servicio.objects.exclude(id=servicio_slug)

    image_one = Image.open(servicio.imagen.path).convert('RGB')

    for servicio_comp in comparativas:
        try:
            image_two = Image.open(servicio_comp.imagen.path).convert('RGB')
            diff = ImageChops.difference(image_one, image_two)
            if not diff.getbbox():
                return True

        except FileNotFoundError:
            continue

    return False

def verificar_formato_imagen(imagen):
    try:
        formato = imagen.name.split('.')[-1].lower()
        if formato not in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tif', 'tiff', 'webp', 'ico', 'svg']:
            mensaje_error = "Formato de imagen inválido. Los formatos admitidos son: .jpg, .jpeg, .png, .gif, .bmp, .tif, .tiff, .webp, .ico, .svg"
            return False, mensaje_error
        return True, None
    except AttributeError:
        raise ValidationError("Se produjo un error al verificar el formato de la imagen.")   
    
@soy_cliente
def ver_imagen_view(request, slug):
    servicio = Servicio.objects.get(slug=slug)
    if request.method == "POST":
        accion = request.POST.get('accion')
        if accion == 'cancelar':
            servicio.delete()
            messages.success(request, "Publicacion de servicio cancelada con éxito")
            return redirect("listar_solicitudes")
    context = {
        'servicio': servicio,
    }
    return render(request, "gestion_de_servicios/ver_imagen.html", context)

@soy_cliente
def pagar_publicacion_view(request, slug):
    servicio = Servicio.objects.get(slug=slug)
    if request.method == 'POST':
        numero_tarjeta = request.POST.get('numero_tarjeta')
        nombre_dueño = request.POST.get('nombre_dueño')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')
        codigo_seguridad = request.POST.get('codigo_seguridad')
        monto = 100  # Asumiendo que el modelo Servicio tiene un campo 'precio'
        
        # Validación básica
        if not all([numero_tarjeta, nombre_dueño, fecha_vencimiento, codigo_seguridad]):
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('pagar_publicacion', slug=slug)
        
        
        if numero_tarjeta[0] in ('4', '5'):        
            fecha_vencimiento = str(fecha_vencimiento)
            if isinstance(fecha_vencimiento, str):
                partes = fecha_vencimiento.split('/')
                if len(partes) == 2:
                    mes, año = partes
                    mes_vencimiento = int(mes)
                    año_vencimiento = int(año)
                else:
                    print(partes)
                    print(len(partes))
                    messages.error(request, "Len no es 2.")
                    return redirect('pagar_publicacion', slug=slug)
            else:
                messages.error(request, "No es string.")
                return redirect('pagar_publicacion', slug=slug)
            tarjeta = Tarjeta.objects.get(numero=numero_tarjeta)    
            if (tarjeta):
                if (tarjeta.nombre_apellido != nombre_dueño): 
                    messages.error(request, "El nombre ingresado no coincide con el nombre del dueño de la tarjeta.")
                    return redirect('pagar_publicacion', slug=slug)
                if (tarjeta.mes_vencimiento != mes_vencimiento or tarjeta.año_vencimiento != año_vencimiento):
                    messages.error(request, "La fecha ingresada no coincide con la fecha de vencimiento de la tarjeta.")
                    return redirect('pagar_publicacion', slug=slug)
                if (tarjeta.mes_vencimiento < 7 and tarjeta.año_vencimiento <= 2024):
                    messages.error(request, "La tarjeta caducó.")
                    return redirect('pagar_publicacion', slug=slug)                
                if (tarjeta.cvv != codigo_seguridad):
                    messages.error(request, "El codigo ingresado no coincide con el codigo de seguridad de la tarjeta.")
                    return redirect('pagar_publicacion', slug=slug)
                if (tarjeta.saldo < monto):
                    messages.error(request, "El saldo de la tarjeta es insuficiente.")
                    return redirect('pagar_publicacion', slug=slug)
            else :
                messages.error(request, "Esta tarjeta no se encuentra registrada en el sistema.")
                return redirect('pagar_publicacion', slug=slug)        
            
            # Crear una nueva instancia de PagoServicio
            pago = PagoServicio(
                cliente=request.user,
                monto=monto,
                fecha=datetime.now().date(),  # Establecer la fecha actual para el pago
                tarjeta=tarjeta
            )
            servicio.estado = 'publicado'
            servicio.save()
            pago.save()

            messages.success(request, "Pago realizado con éxito.")
            return redirect('listar_solicitudes')  # Redirige a una página de éxito o donde desees
        else:
            messages.error(request, "Solo se aceptan tarjetas Visa o MasterCard.")
            return redirect('pagar_publicacion', slug=slug)
    context = {
        'servicio': servicio,
    }
    return render(request, "gestion_de_servicios/pagar_publicacion.html", context)

@super_user 
def listar_solicitudes_clientes_view(request):    
    queryset = Servicio.objects.filter(estado = "pendiente")
    context = {
        "lista": queryset
    }
    
    return render(request, "gestion_de_servicios/listar_solicitudes_clientes.html", context)

@super_user 
def evaluar_servicio_view(request, slug):
    servicio = Servicio.objects.get(slug=slug)
    if request.method == "POST":
        accion = request.POST.get('accion')
        if accion == 'aceptar':
            servicio.estado = 'aceptado'
            servicio.save()
            messages.success(request, "El servicio ha sido aceptado.")
            return redirect("listar_solicitudes_clientes")
        elif accion == 'rechazar':
            return redirect("mandar_motivo", slug=slug)
    context = {
        'servicio': servicio,
    }
    return render(request, "gestion_de_servicios/evaluar_servicio.html", context)

@super_user 
def mandar_motivo_view(request, slug):
    servicio = Servicio.objects.get(slug=slug)
    if request.method == "POST":
        motivo = request.POST.get('motivo')
        if not motivo.strip():
            messages.error(request, "Completa la casilla de texto, el motivo no puede estar vacio")
        else:
            servicio.estado = 'rechazado'
            servicio.save()
            cliente = servicio.cliente
            subject = 'Rechazo de Servicio'
            message = f'Hola {cliente.username},\n\nTu solicitud de publicacion ha sido rechazada, este es el motivo:\n\n{motivo}\n\n'
            from_email = 'noreply@ferreplus.com'
            to_email = [cliente.email]
            send_mail(subject, message, from_email, to_email)
            messages.success(request, "El servicio ha sido rechazado.")
            return redirect("listar_solicitudes_clientes")
    context = {
        'servicio': servicio
    }
    return render(request, "gestion_de_servicios/mandar_motivo.html", context)

def servicios_publicados_view(request):
    print("llego")
    servicios_publicados = Servicio.objects.filter(estado='publicado')
    return render(request, 'gestion_de_servicios/servicios_publicados.html', {'servicios': servicios_publicados})