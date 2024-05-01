from django.shortcuts import render
from .models import *

# Create your views here.

def gestion_de_sucursales_view (request):
    return render(request, "gestion_de_sucursales/gestion_sucursales.html")

def agregar_sucursal_view (request):
    return render(request, "gestion_de_sucursales/agregar_sucursal.html")

def insertar_sucursal_view (request):
    if request.method == "POST":
        nombre = request.POST["sucursal"]
        ciudad = request.POST["ciudad"]

        nueva_sucursal = Sucursal(nombre=nombre, ciudad=ciudad)
        nueva_sucursal.save()

    return render(request, "gestion_de_sucursales/gestion_sucursales.html") 

def listar_sucursales_view (request):
    queryset = Sucursal.objects.all()
    context= {
        "lista": queryset
    }
    return render (request, "gestion_de_sucursales/listar_sucursales.html", context)