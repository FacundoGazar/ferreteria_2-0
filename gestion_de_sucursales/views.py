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


def eliminar_sucursal_view (request):
    sucursales = Sucursal.objects.all()

    return render (request,"gestion_de_sucursales/eliminar_sucursal.html",{'sucursales': sucursales})


def delete_sucursal_view(request):
    if request.method == 'POST':
        nombre_sucursal = request.POST.get('sucursal')
        
        if nombre_sucursal:
            try:
                sucursal = Sucursal.objects.get(nombre=nombre_sucursal)
                sucursal.delete()
                return render(request, "gestion_de_sucursales/gestion_sucursales.html")
            except Sucursal.DoesNotExist:
                return render(request, 'error.html', {'mensaje': 'La sucursal seleccionada no existe.'})
        else:
            return render(request, 'error.html', {'mensaje': 'No se proporcionó una sucursal para eliminar.'})
    else:

        return render(request, 'error.html', {'mensaje': 'Solicitud no válida.'})