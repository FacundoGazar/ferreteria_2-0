from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from iniciar_sesion import not_super_user
from .forms import ProductoForm
from .models import Producto
# Create your views here.

@not_super_user
def mis_productos_view(request):
    return render (request, "mis_productos/mis_productos.html")

@not_super_user
def subir_producto_view(request):
    subido = False
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.cliente = request.user
            producto.save()
            return HttpResponseRedirect(reverse("subir_producto") + "?subido=True")
    else:
        form = ProductoForm
        if "subido" in request.GET:
            subido = True
    return render (request, "mis_productos/subir_producto.html", {"form": form, "subido": subido})

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
