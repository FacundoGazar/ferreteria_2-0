from django.shortcuts import render
from gestion_de_sucursales.models import Sucursal
from mis_productos.models import Producto
from intercambiar_producto.models import Intercambio
# Create your views here.

def homepage_view(request):
    return render(request, "homepage/homepage.html")

def tu_vista(request):
    # Obtener todos los productos excluyendo los del usuario actual
    if request.user.is_authenticated:
        lista_productos = Producto.objects.exclude(cliente=request.user)
    else:
        lista_productos = Producto.objects.all()
    
    # Excluir productos en intercambios aceptados
    intercambios_aceptados_o_realizados = Intercambio.objects.filter(estado__in=['aceptado', 'realizado']).values_list('producto_solicitante', 'producto_receptor')
    productos_excluir = set()
    for productos in intercambios_aceptados_o_realizados:
        productos_excluir.update(productos)

    lista_productos = lista_productos.exclude(id__in=productos_excluir)

    contexto = {
        'lista_productos': lista_productos
    }

    return render(request, "homepage/homepage.html", contexto)

