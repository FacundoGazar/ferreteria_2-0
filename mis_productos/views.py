from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProductoForm
from .models import Producto
from iniciar_sesion import soy_cliente
# Create your views here.

@soy_cliente
def mis_productos_view(request):
    return render (request, "mis_productos/mis_productos.html")

@soy_cliente
def subir_producto_view(request):
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
    return render (request, "mis_productos/subir_producto.html", {"form": form}) 

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
