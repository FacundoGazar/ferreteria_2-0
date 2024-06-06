from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProductoForm
from gestion_de_sucursales.models import Sucursal
from .models import Producto
from iniciar_sesion import soy_cliente
from intercambiar_producto.models import Intercambio
from django.core.exceptions import ValidationError
from PIL import Image, ImageChops
import re
from django.db.models import Q

# Create your views here.

@soy_cliente
def mis_productos_view(request):
    return render (request, "mis_productos/mis_productos.html")

@soy_cliente
def subir_producto_view(request):
    sucursales = Sucursal.objects.all()
    estados_list = ["Nuevo - Sin uso", "Usado", "Restaurado", "Para reparar", "Para piezas", "Con defectos leves"]
    categorias_list = ["Herramientas", "Construcción", "Ferretería general", "Electricidad", "Fontanería", "Jardín"]
    dias_list = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    horarios_list = ["9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)

        imagen_principal = request.FILES.get('imagen_principal')
        if imagen_principal:
            formato_valido, mensaje_error = verificar_formato_imagen(imagen_principal)
            if not formato_valido:
                messages.error(request, mensaje_error)
                return render(request, "mis_productos/subir_producto.html", {
                    "form": form,
                    "sucursales": sucursales,
                    "categorias_list": categorias_list,
                    "estados_list": estados_list,
                    "dias_list": dias_list,
                    "horarios_list_inicio": horarios_list[:8],
                    "horarios_list_fin": horarios_list[1:]
                })
        else:
            messages.error(request, "Es obligatorio subir al menos una imagen para el producto.")
            return render(request, "mis_productos/subir_producto.html", {
                    "form": form,
                    "sucursales": sucursales,
                    "categorias_list": categorias_list,
                    "estados_list": estados_list,
                    "dias_list": dias_list,
                    "horarios_list_inicio": horarios_list[:8],
                    "horarios_list_fin": horarios_list[1:]
                })

        for campo_imagen in ['imagen_extra1', 'imagen_extra2', 'imagen_extra3']:
            imagen = request.FILES.get(campo_imagen)
            if imagen:
                formato_valido, mensaje_error = verificar_formato_imagen(imagen)
                if not formato_valido:
                    messages.error(request, mensaje_error)
                    return render(request, "mis_productos/subir_producto.html", {
                        "form": form,
                        "sucursales": sucursales,
                        "categorias_list": categorias_list,
                        "estados_list": estados_list,
                        "dias_list": dias_list,
                        "horarios_list_inicio": horarios_list[:8],
                        "horarios_list_fin": horarios_list[1:]
                    })
                    
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            if not re.search('[a-zA-Z]{1,}', nombre):
                messages.error(request, "El nombre debe contener al menos una letra.")
                return render(request, "mis_productos/subir_producto.html", {
                    "form": form,
                    "sucursales": sucursales,
                    "categorias_list": categorias_list,
                    "estados_list": estados_list,
                    "dias_list": dias_list,
                    "horarios_list_inicio": horarios_list[:8],
                    "horarios_list_fin": horarios_list[1:]
                })
            
            producto = form.save(commit=False)
            producto.cliente = request.user
            producto.save()

            if are_images_equal(producto.slug):
                producto.delete()
                messages.error(request, "¡Este producto ya fue publicado en el sitio!")
            else:
                messages.success(request, "¡Se ha subido el producto correctamente!")
            return redirect("mis_productos")
        
    else:
        form = ProductoForm()

    return render(request, "mis_productos/subir_producto.html", {
        "form": form,
        "sucursales": sucursales,
        "categorias_list": categorias_list,
        "estados_list": estados_list,
        "dias_list": dias_list,
        "horarios_list_inicio": horarios_list[:8],
        "horarios_list_fin": horarios_list[1:]
    })

def are_images_equal(producto_slug):
    producto = Producto.objects.get(slug=producto_slug)
    comparativas = Producto.objects.exclude(slug=producto_slug)

    image_one = Image.open(producto.imagen_principal.path).convert('RGB')

    for producto_comp in comparativas:
        try:
            image_two = Image.open(producto_comp.imagen_principal.path).convert('RGB')
            diff = ImageChops.difference(image_one, image_two)
            if not diff.getbbox():
                return True

            for extra_image_field in ['imagen_extra1', 'imagen_extra2', 'imagen_extra3']:
                extra_image = getattr(producto, extra_image_field, None)
                if extra_image:
                    image_extra = Image.open(extra_image.path).convert('RGB')
                    diff_extra = ImageChops.difference(image_extra, image_two)
                    if not diff_extra.getbbox():
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
def eliminar_producto_view(request):
    productos = Producto.objects.filter(cliente=request.user)
    intercambios_aceptados_o_realizados = Intercambio.objects.filter(estado__in=['aceptado', 'realizado'])
    productos_intercambio_ids = []
    for intercambio in intercambios_aceptados_o_realizados:
        productos_intercambio_ids.append(intercambio.producto_solicitante_id)
        productos_intercambio_ids.append(intercambio.producto_receptor_id)
    productos = productos.exclude(id__in=productos_intercambio_ids)
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        
        if producto_id:
            producto = Producto.objects.get(id=producto_id)
            producto.delete()
            messages.success(request, "Producto eliminado con éxito")
        else:
            messages.error(request, "Seleccione un producto")

    return render (request, "mis_productos/eliminar_producto.html",{'productos': productos})

@soy_cliente
def listar_mis_productos_view(request):
    usuario = request.user
    queryset = Producto.objects.filter(cliente=usuario, visible=True)
    if queryset.filter(sucursal__isnull=True).exists():
        messages.warning(request, "Tenes al menos un producto en una sucursal inactiva. Por favor, asignale una nueva sucursal.")

    context = {
        "lista": queryset
    }
    
    return render(request, "mis_productos/listar_mis_productos.html", context)

@soy_cliente
def ver_detalle_view(request, slug):
    producto = Producto.objects.get(slug=slug)
    tiene_intercambio = Intercambio.objects.filter(
       estado='aceptado',
       producto_solicitante=producto
    ).exists() or Intercambio.objects.filter(
       estado='aceptado',
       producto_receptor=producto
    ).exists()
    
    return render(request, 'mis_productos/ver_detalle.html', {
        'producto': producto,
        'tiene_intercambio': tiene_intercambio
    })

@soy_cliente
def modificar_producto_view(request, slug):
    producto = Producto.objects.get(slug=slug)
    productoViejo = Producto.objects.get(slug=slug)
    sucursales = Sucursal.objects.all()
    estados_list = ["Nuevo - Sin uso", "Usado", "Restaurado", "Para reparar", "Para piezas", "Con defectos leves"]
    categorias_list = ["Herramientas", "Construcción", "Ferretería general", "Electricidad", "Fontanería", "Jardín"]
    dias_list = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    horarios_list = ["9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        imagen_principal = request.FILES.get('imagen_principal')
        if imagen_principal:
            formato_valido, mensaje_error = verificar_formato_imagen(imagen_principal)
            if not formato_valido:
                messages.error(request, mensaje_error)
                return render(request, "mis_productos/modificar_producto.html", {
                    "form": form,
                    'imagen_principal': producto.imagen_principal.url if producto.imagen_principal else None,
                    'imagen_extra1': producto.imagen_extra1.url if producto.imagen_extra1 else None,
                    'imagen_extra2': producto.imagen_extra2.url if producto.imagen_extra2 else None,
                    'imagen_extra3': producto.imagen_extra3.url if producto.imagen_extra3 else None,
                    "sucursales": sucursales,
                    "categorias_list": categorias_list,
                    "estados_list": estados_list,
                    "dias_list": dias_list,
                    "horarios_list_inicio": horarios_list[:8],
                    "horarios_list_fin": horarios_list[1:]
                })
        else:
            imagen_principal = productoViejo.imagen_principal

        for campo_imagen in ['imagen_extra1', 'imagen_extra2', 'imagen_extra3']:
            imagen = request.FILES.get(campo_imagen)
            if imagen:
                formato_valido, mensaje_error = verificar_formato_imagen(imagen)
                if not formato_valido:
                    messages.error(request, mensaje_error)
                    return render(request, "mis_productos/modificar_producto.html", {
                        "form": form,
                        'imagen_principal': producto.imagen_principal.url if producto.imagen_principal else None,
                        'imagen_extra1': producto.imagen_extra1.url if producto.imagen_extra1 else None,
                        'imagen_extra2': producto.imagen_extra2.url if producto.imagen_extra2 else None,
                        'imagen_extra3': producto.imagen_extra3.url if producto.imagen_extra3 else None,
                        "sucursales": sucursales,
                        "categorias_list": categorias_list,
                        "estados_list": estados_list,
                        "dias_list": dias_list,
                        "horarios_list_inicio": horarios_list[:8],
                        "horarios_list_fin": horarios_list[1:]
                    })
                    
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            if not re.search('[a-zA-Z]{1,}', nombre):
                messages.error(request, "El nombre debe contener al menos una letra.")
                horario_inicio = producto.horario_inicio
                horario_fin = producto.horario_fin
                horarios_list_fin = horarios_list[horarios_list.index(horario_inicio)+1:] if horario_inicio else []
                return render(request, "mis_productos/modificar_producto.html", {
                    "form": form,
                    'imagen_principal': producto.imagen_principal.url if producto.imagen_principal else None,
                    'imagen_extra1': producto.imagen_extra1.url if producto.imagen_extra1 else None,
                    'imagen_extra2': producto.imagen_extra2.url if producto.imagen_extra2 else None,
                    'imagen_extra3': producto.imagen_extra3.url if producto.imagen_extra3 else None,
                    "sucursales": sucursales,
                    "categorias_list": categorias_list,
                    "estados_list": estados_list,
                    "dias_list": dias_list,
                    "horarios_list_inicio": horarios_list[:8],
                    "horarios_list_fin": horarios_list_fin
                })
            
            if 'imagen_principal' in request.FILES:
                producto.imagen_principal = request.FILES['imagen_principal']
            if 'imagen_extra1' in request.FILES:
                producto.imagen_extra1 = request.FILES['imagen_extra1']
            if 'imagen_extra2' in request.FILES:
                producto.imagen_extra2 = request.FILES['imagen_extra2']
            if 'imagen_extra3' in request.FILES:
                producto.imagen_extra3 = request.FILES['imagen_extra3']
            if 'eliminar_imagen_extra1' in request.POST:
                producto.imagen_extra1.delete()
                producto.imagen_extra1 = None
            if 'eliminar_imagen_extra2' in request.POST:
                producto.imagen_extra2.delete()
                producto.imagen_extra2 = None
            if 'eliminar_imagen_extra3' in request.POST:
                producto.imagen_extra3.delete()
                producto.imagen_extra3 = None
            producto = form.save(commit=False)
            producto.cliente = request.user
            producto.save()    
            
            if are_images_equal(producto.slug):
                producto=productoViejo
                producto.save()  
                messages.error(request, "¡Este producto ya fue publicado en el sitio!")
            else:
                form.save()
                messages.success(request, "¡Se ha subido el producto correctamente!")
            return redirect("mis_productos")
        else:
            form = ProductoForm(instance=producto)
            messages.error(request, "Por favor, completa el nombre.")
    else:
        form = ProductoForm(instance=producto)
        horario_inicio = producto.horario_inicio
        horario_fin = producto.horario_fin
        horarios_list_fin = horarios_list[horarios_list.index(horario_inicio)+1:] if horario_inicio else []
    horario_inicio = producto.horario_inicio
    horario_fin = producto.horario_fin
    horarios_list_fin = horarios_list[horarios_list.index(horario_inicio)+1:] if horario_inicio else []

    return render(request, "mis_productos/modificar_producto.html", {
        "form": form,
        'imagen_principal': producto.imagen_principal.url if producto.imagen_principal else None,
        'imagen_extra1': producto.imagen_extra1.url if producto.imagen_extra1 else None,
        'imagen_extra2': producto.imagen_extra2.url if producto.imagen_extra2 else None,
        'imagen_extra3': producto.imagen_extra3.url if producto.imagen_extra3 else None,
        "sucursales": sucursales,
        "categorias_list": categorias_list,
        "estados_list": estados_list,
        "dias_list": dias_list,
        "horarios_list_inicio": horarios_list[:8],
        "horarios_list_fin": horarios_list_fin
    })




