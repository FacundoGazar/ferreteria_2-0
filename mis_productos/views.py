from django.shortcuts import render

# Create your views here.

def mis_productos_view(request):
    return render (request, "mis_productos/mis_productos.html")

def subir_producto_view(request):
    return render (request, "mis_productos/subir_producto.html")

def eliminar_producto_view(request):
    return render (request, "mis_productos/eliminar_producto.html")

def listar_mis_productos_view(request):
    return render (request, "mis_productos/listar_mis_productos.html")

def ver_detalle_view(request):
    return render (request, "mis_productos/ver_detalle.html")