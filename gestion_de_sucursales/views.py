from django.shortcuts import render
from .models import *
from django.contrib import messages

# Create your views here.

def gestion_de_sucursales_view (request):
    return render(request, "gestion_de_sucursales/gestion_sucursales.html")

def agregar_sucursal_view (request):
    return render(request, "gestion_de_sucursales/agregar_sucursal.html")

def insertar_sucursal_view (request):
    if request.method == "POST":
        nombre = request.POST["sucursal"]
        if Sucursal.objects.filter(nombre=nombre).exists():
            messages.success(request, ("Nombre de sucursal ya existente"))
            return render(request, "gestion_de_sucursales/agregar_sucursal.html") 
        else:
            ciudad = request.POST["ciudad"]
            nueva_sucursal = Sucursal(nombre=nombre, ciudad=ciudad)
            nueva_sucursal.save()            
            return render(request, "gestion_de_sucursales/gestion_sucursales.html") 
    
    return render(request, "gestion_de_sucursales/gestion_sucursales.html") 
    

def listar_sucursales_view(request):
    queryset = Sucursal.objects.all()
    
    context = {
        "lista": queryset
    }

    return render(request, "gestion_de_sucursales/listar_sucursales.html", context)
