from django.shortcuts import render
from gestion_de_sucursales.models import Sucursal
from mis_productos.models import Producto
# Create your views here.

def homepage_view(request):
    return render(request, "homepage/homepage.html")

def tu_vista(request):
    # Obtener todos los productos excluyendo los del usuario actual
    if request.user.is_authenticated:
        lista_productos = Producto.objects.exclude(cliente=request.user)
    else:
        lista_productos = Producto.objects.all()

    contexto = {
        'lista_productos': lista_productos
    }

    return render(request, "homepage/homepage.html", contexto)

