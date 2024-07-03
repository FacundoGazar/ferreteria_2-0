from django.shortcuts import render,get_object_or_404, redirect
from .models import *
from django.contrib import messages
from iniciar_sesion import super_user
import json
from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

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
    # Obtener todas las sucursales
    queryset = Sucursal.objects.all()

    # Obtener ciudades únicas
    ciudades = Sucursal.objects.values_list('ciudad', flat=True).distinct()

    # Filtrar por ciudad si se recibe el parámetro en GET
    ciudad_seleccionada = request.GET.get('ciudad')
    if ciudad_seleccionada:
        queryset = queryset.filter(ciudad=ciudad_seleccionada)

    context = {
        "lista": queryset,
        "ciudades": ciudades  # Pasa las ciudades como contexto
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
                if sucursal.perfilempleado_set.exists():
                    messages.error(request, "No se puede eliminar la sucursal porque hay empleados asignados a ella")
                elif Sucursal.objects.count() == 1:
                    messages.error(request, "No se puede eliminar la única sucursal que existe")
                else:
                    sucursal.delete()
                    messages.success(request, "Sucursal eliminada con éxito")
            except Sucursal.DoesNotExist:
                messages.error(request, ("No existe la sucursal"))
            return redirect('eliminar_sucursal')
        else:
            messages.error(request, ("No se selecciono sucursal"))
            return redirect('eliminar_sucursal')
    else:

        messages.error(request, ("Solicitud Invalida"))
        return redirect('eliminar_sucursal')
    
@super_user 
def gestion_de_empleados_view(request):
    empleados = PerfilEmpleado.objects.all()

    # Obtener el nombre de la sucursal seleccionada si existe
    nombre_sucursal_seleccionada = request.GET.get('sucursal')

    # Filtrar empleados por sucursal si se proporciona el nombre de la sucursal
    if nombre_sucursal_seleccionada:
        sucursal_seleccionada = get_object_or_404(Sucursal, nombre=nombre_sucursal_seleccionada)
        empleados = empleados.filter(sucursal=sucursal_seleccionada)
    
    # Obtener todas las sucursales
    sucursales = Sucursal.objects.all()
    
    if not empleados:
        messages.info(request, "No hay empleados registrados.")
    
    return render(request, "gestion_de_sucursales/gestion_de_empleados.html", {'empleados': empleados, 'nombre_sucursal_seleccionada': nombre_sucursal_seleccionada, 'sucursales': sucursales})

# revisar

@super_user
def lista_empleados_view(request):
    sucursal_seleccionada = request.GET.get('sucursal')
    
    if sucursal_seleccionada:
        empleados = PerfilEmpleado.objects.filter(sucursal_id=sucursal_seleccionada)
    else:
        empleados = PerfilEmpleado.objects.all()
    
    sucursales = Sucursal.objects.all()
    
    return render(request, 'nombre_de_tu_template.html', {
        'empleados': empleados,
        'sucursales': sucursales,
        'sucursal_seleccionada': int(sucursal_seleccionada) if sucursal_seleccionada else None
    })

@super_user 
def dar_de_baja_view(request):
    sucursales = Sucursal.objects.all()
    empleados = PerfilEmpleado.objects.all()
    empleados_json = json.dumps(list(empleados.values('dni', 'sucursal')))
    return render(request, 'gestion_de_sucursales/dar_de_baja.html', {'sucursales': sucursales, 'empleados_json': empleados_json})

@super_user 
def trasladar_empleado_view(request):
    sucursales = Sucursal.objects.all()
    empleados = PerfilEmpleado.objects.all()
    return render(request, 'gestion_de_sucursales/trasladar_empleado.html', {'sucursales': sucursales, 'empleados': empleados})

@super_user
def trasladar_view (request):
    if request.method == 'POST':
        emp_dni = request.POST.get('dni')
        nueva_sucursal_nombre = request.POST.get('sucursal')
        

        if emp_dni:
            try:
                empleado= PerfilEmpleado.objects.get(dni=emp_dni)
                nueva_sucursal = Sucursal.objects.get(nombre=nueva_sucursal_nombre)
                print(nueva_sucursal)
                empleado.sucursal= nueva_sucursal
                print(empleado.sucursal.nombre)
                empleado.save()  # Guarda los cambios en la base de datos
                messages.success(request, "Empleado trasladado con éxito")
            except PerfilEmpleado.DoesNotExist:
                messages.error (request,'No se encontro el empleado')
            return redirect ('trasladar_empleado')
        else:
            messages.error(request, ("No se selecciono empleado"))
            return redirect('trasladar_empleado')
    else:
        messages.error(request, ("Solicitud Invalida"))
        return redirect('trasladar_empleado')

@super_user
def eliminar_empleado_view (request):
    if request.method == 'POST':
        emp_dni = request.POST.get('dni')

        if emp_dni:
            try:
                empleado= PerfilEmpleado.objects.get(dni=emp_dni)
                empleado.usuario.delete()
                empleado.delete()
                messages.error(request, ("Empleado dado de baja"))
            except PerfilEmpleado.DoesNotExist:
                messages.error (request,'No se encontro el empleado')
            return redirect ('dar_de_baja')
        else:
            messages.error(request, ("No se selecciono empleado"))
            return redirect('dar_de_baja')
    else:
        messages.error(request, ("Solicitud Invalida"))
        return redirect('dar_de_baja')


@super_user 
def agregar_empleado_view(request):
    sucursales = Sucursal.objects.all()
    return render(request, "gestion_de_sucursales/agregar_empleado.html", {'sucursales': sucursales})

@super_user 
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
        if PerfilEmpleado.objects.filter(dni=dni).exists():
            messages.error(request, "El DNI ya está registrado para otro empleado")
            return redirect('agregar_empleado')
        
        try:
             validate_password(contrasenia)
        except ValidationError as error:
            messages.success(request, "La contraseña no cumple con los requisitos")
            return redirect('agregar_empleado')


        nuevo_usuario = User.objects.create_user(username=usuario, email=email, password=contrasenia, is_staff=True)
        perfil_empleado = PerfilEmpleado(usuario=nuevo_usuario, nombre = nombre, dni = dni, sucursal = sucursal  )
        perfil_empleado.save()
        subject = 'Registro de empleado en Ferreplus'
        message = f'Hola {nombre},\n\nTu cuenta de empleado en Ferreplus ha sido creada.\n\nNombre de usuario: {usuario}\nContraseña: {contrasenia}\n\n¡Gracias!'
        from_email = 'noreply@ferreplus.com'
        to_email = [email]
        send_mail(subject, message, from_email, to_email)

        messages.success(request, "Se registró el usuario y se envió un correo electrónico con los detalles de la cuenta")

        return redirect('agregar_empleado')
    
