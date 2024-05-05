from django.shortcuts import render, redirect
from django.contrib import messages
from iniciar_sesion import not_super_user
from .forms import ProductoForm
from .models import Producto
# Create your views here.

@not_super_user
def mis_productos_view(request):
    return render (request, "mis_productos/mis_productos.html")

@not_super_user
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

@not_super_user
def eliminar_producto_view(request):
    return render (request, "mis_productos/eliminar_producto.html")

@not_super_user
def listar_mis_productos_view(request):
    usuario = request.user
    queryset = Producto.objects.filter(cliente=usuario)
    
    context = {
        "lista": queryset
    }
    
    return render(request, "mis_productos/listar_mis_productos.html", context)

@not_super_user
def ver_detalle_view(request, slug):
    producto = Producto.objects.get(slug=slug)
    return render(request, 'mis_productos/ver_detalle.html', {'producto': producto})
