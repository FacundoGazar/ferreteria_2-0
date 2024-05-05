from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from iniciar_sesion import super_user
import json

# Create your views here.

@super_user
def gestion_de_sucursales_view (request):
    return render(request, "gestion_de_sucursales/gestion_sucursales.html")

@super_user
def agregar_sucursal_view (request):
    if request.method == "POST":
        nombre = request.POST["sucursal"]
        ciudad = request.POST["ciudad"]
        if Sucursal.objects.filter(nombre=nombre).exists():
            messages.error(request, ("Nombre de sucursal ya existente"))
            return redirect("agregar_sucursal")
        elif(len(nombre) < 1 or len(ciudad) < 1):
            messages.error(request, ("Debe completar todos los campos."))
            return redirect("agregar_sucursal")
        else:
            nueva_sucursal = Sucursal(nombre=nombre, ciudad=ciudad)
            nueva_sucursal.save()
            return redirect("gestion_de_sucursales")
        
    return render(request, "gestion_de_sucursales/agregar_sucursal.html")
    
@super_user
def listar_sucursales_view(request):
    queryset = Sucursal.objects.all()
    
    context = {
        "lista": queryset
    }

    return render(request, "gestion_de_sucursales/listar_sucursales.html", context)

@super_user
def eliminar_sucursal_view (request):
    sucursales = Sucursal.objects.all()

    return render (request,"gestion_de_sucursales/eliminar_sucursal.html",{'sucursales': sucursales})

@super_user
def delete_sucursal_view(request):
    if request.method == 'POST':
        nombre_sucursal = request.POST.get('sucursal')
        
        if nombre_sucursal:
            try:
                sucursal = Sucursal.objects.get(nombre=nombre_sucursal)
                sucursal.delete()
                messages.error(request, ("Sucursal eliminada con exito"))
            except Sucursal.DoesNotExist:
                messages.error(request, ("No existe la sucursal"))
            return redirect('eliminar_sucursal')
        else:
            messages.error(request, ("No se selecciono sucursal"))
            return redirect('eliminar_sucursal')
    else:

        messages.error(request, ("Solicitud Invalida"))
        return redirect('eliminar_sucursal')
    
def gestion_de_empleados_view (request):
    empleados = PerfilEmpleado.objects.all()
    return render(request, "gestion_de_sucursales/gestion_de_empleados.html",{'empleados': empleados})

def dar_de_baja_view(request):
    sucursales = Sucursal.objects.all()
    empleados = PerfilEmpleado.objects.all()
    empleados_json = json.dumps(list(empleados.values('dni', 'sucursal')))
    return render(request, 'gestion_de_sucursales/dar_de_baja.html', {'sucursales': sucursales, 'empleados_json': empleados_json})

def agregar_empleado_view(request):
    sucursales = Sucursal.objects.all()
    return render(request, "gestion_de_sucursales/agregar_empleado.html", {'sucursales': sucursales})

def registrar_empleado (request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        contrasenia = request.POST.get('password')
        dni = request.POST.get('dni')
        nombre_sucursal = request.POST.get('sucursal')
        try:
            sucursal = Sucursal.objects.get(nombre=nombre_sucursal)
        except Sucursal.DoesNotExist:
            messages.error(request, "La sucursal seleccionada no existe")
            return redirect('agregar_empleado')     
        if User.objects.filter(username=usuario).exists():
            messages.error(request, "El nombre de usuario ya se encuentra registrado")
            return redirect('agregar_empleado')       

        nuevo_usuario = User.objects.create_user(username=usuario, email=email, password=contrasenia)
        perfil_empleado = PerfilEmpleado(usuario=nuevo_usuario, nombre = nombre, dni = dni, sucursal = sucursal  )
        perfil_empleado.save()
        messages.success(request, "Se registro el usuario")

        return redirect('agregar_empleado')   