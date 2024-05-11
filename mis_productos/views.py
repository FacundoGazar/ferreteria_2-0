from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProductoForm
from gestion_de_sucursales.models import Sucursal
from .models import Producto
from iniciar_sesion import soy_cliente
import json

# Create your views here.

@soy_cliente
def mis_productos_view(request):
    return render (request, "mis_productos/mis_productos.html")

@soy_cliente
def subir_producto_view(request):
    sucursales= Sucursal.objects.all()
    estados_list = ["Nuevo - Sin uso", "Usado", "Restaurado", "Para reparar", "Para piezas", "Con defectos leves"]
    categorias_list = ["Herramientas", "Construcción", "Ferretería general", "Electricidad", "Fontanería", "Jardín"]
    horarios_list = ["9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.cliente = request.user
            producto.save()
            messages.success(request, ("¡¡ Se ha subido el producto correctamente !!"))
            return redirect("mis_productos")
    else:
        form = ProductoForm
    return render (request, "mis_productos/subir_producto.html", {
        "form": form,
        "sucursales": sucursales, 
        "categorias_list": categorias_list, 
        "estados_list": estados_list,
        "horarios_list_inicio": horarios_list[:8],
        "horarios_list_fin": horarios_list[1:]}) 

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
