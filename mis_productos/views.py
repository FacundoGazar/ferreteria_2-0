from django.shortcuts import render
from .decoradores import *

# Create your views here.

@not_super_user
def mis_productos_view(request):
    return render (request, "mis_productos/mis_productos.html")

@not_super_user
def subir_producto_view(request):
    return render (request, "mis_productos/subir_producto.html")

@not_super_user
def eliminar_producto_view(request):
    return render (request, "mis_productos/eliminar_producto.html")

@not_super_user
def listar_mis_productos_view(request):
    return render (request, "mis_productos/listar_mis_productos.html")

@not_super_user
def ver_detalle_view(request):
    return render (request, "mis_productos/ver_detalle.html")