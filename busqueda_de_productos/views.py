from django.shortcuts import render
from mis_productos.models import Producto
from rest_framework import viewsets, filters
from mis_productos.models import Producto
from django.contrib.auth.models import User

def buscar_productos2(request):
    usuario_actual = request.user
    if hasattr(usuario_actual, 'perfilcliente'):
        queryset = Producto.objects.exclude(cliente=usuario_actual)
    else: 
        queryset = Producto.objects.all()

    # Capturar el parámetro de búsqueda
    busqueda = request.GET.get('busqueda')
    if busqueda:
        queryset = queryset.filter(nombre__icontains=busqueda)

    context = {
        "lista": queryset
    }
    return render(request, "busqueda_de_productos/buscar_productos.html", context)
from django.db.models import Q

def buscar_productos(request):
    usuario_actual = request.user
    if hasattr(usuario_actual, 'perfilcliente'):
        queryset = Producto.objects.exclude(cliente=usuario_actual)
    else: 
        queryset = Producto.objects.all()

    # Capturar el parámetro de búsqueda
    busqueda = request.GET.get('busqueda')

    # Filtrar por categoría
    categorias = request.GET.getlist('categoria')
    if categorias:
        queryset = queryset.filter(categoria__in=categorias)

    # Filtrar por estado
    estados = request.GET.getlist('estado')
    if estados:
        queryset = queryset.filter(estado__in=estados)

    # Filtrar por sucursal
    sucursales = request.GET.getlist('sucursal')
    if sucursales:
        queryset = queryset.filter(sucursal__in=sucursales)

    # Aplicar filtro de búsqueda
    if busqueda:
        queryset = queryset.filter(Q(nombre__icontains=busqueda))

    context = {
        "lista": queryset
    }
    return render(request, "busqueda_de_productos/buscar_productos.html", context)

def ver_detalle(request, slug):
    producto = Producto.objects.get(slug=slug)
    return render(request, 'busqueda_de_productos/ver_detalle_intercambio.html', {'producto': producto})
