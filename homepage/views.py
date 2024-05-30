from django.shortcuts import render
from gestion_de_sucursales.models import Sucursal
from mis_productos.models import Producto
# Create your views here.

def homepage_view(request):
    return render(request, "homepage/homepage.html")

def tu_vista(request):
    sucursales = Sucursal.objects.all()
    estados_list = ["Nuevo - Sin uso", "Usado", "Restaurado", "Para reparar", "Para piezas", "Con defectos leves"]
    categorias_list = ["Herramientas", "Construcción", "Ferretería general", "Electricidad", "Fontanería", "Jardín"]

    contexto = {
        'sucursales': sucursales,
        'estados_list': estados_list,
        'categorias_list': categorias_list
    }

    return render(request, "homepage/homepage.html", contexto)

def mostrar_todos_los_productos(request):
    # Obtener todos los productos excluyendo los del usuario actual
    if request.user.is_authenticated:
        lista_productos = Producto.objects.exclude(cliente=request.user)
    else:
        lista_productos = Producto.objects.all()

    # Pasar la lista de productos al contexto
    contexto = {
        'lista': lista_productos
    }

    # Renderizar la plantilla con el contexto
    return render(request, "homepage/homepage.html", contexto)
