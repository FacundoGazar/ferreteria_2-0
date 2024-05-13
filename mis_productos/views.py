from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProductoForm
from gestion_de_sucursales.models import Sucursal
from .models import Producto
from iniciar_sesion import soy_cliente
from django.core.exceptions import ValidationError
from django.forms import ModelForm
import re

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
                form = ProductoForm(request.POST, request.FILES)
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
            if not re.search('[a-zA-Z]{3,}', nombre):
                messages.error(request, "El nombre debe contener al menos tres letras.")
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
            messages.success(request, "¡Se ha subido el producto correctamente!")
            return redirect("mis_productos")
        
        else:
            messages.error(request, "¡Algo salió mal! Por favor, verifica el formulario.")
    else:
        form = ProductoForm()

    return render(request, "mis_productos/subir_producto.html", {"form": form, "sucursales": sucursales, "categorias_list": categorias_list, "estados_list": estados_list, "dias_list": dias_list, "horarios_list_inicio": horarios_list[:8], "horarios_list_fin": horarios_list[1:]})

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
    queryset = Producto.objects.filter(cliente=usuario)
    
    context = {
        "lista": queryset
    }
    
    return render(request, "mis_productos/listar_mis_productos.html", context)

@soy_cliente
def ver_detalle_view(request, slug):
    producto = Producto.objects.get(slug=slug)
    return render(request, 'mis_productos/ver_detalle.html', {'producto': producto})
