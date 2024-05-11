from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from gestion_de_usuarios.models import PerfilCliente
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from gestion_de_usuarios.forms import FormularioModificarCliente, UserForm
from iniciar_sesion import unauthenticated_user, clienteOEmpleado, authenticated_user
import re
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

@unauthenticated_user
def registrar(request):
    return render(request, 'gestion_de_usuarios/registrar.html')
@unauthenticated_user
def register(request):
    if request.method == 'POST':
        # Obtener los datos del formulario enviado por el usuario
        usuario = request.POST.get('usuario')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        contrasenia = request.POST.get('contrasenia')
        ciudad = request.POST.get('ciudad')
        edad = int(request.POST.get('edad')) 

        # Verificar si la contraseña cumple con los requisitos
        try:
             validate_password(contrasenia)
        except ValidationError as error:
            messages.success(request, "La contraseña no cumple con los requisitos")
            return render(request, 'gestion_de_usuarios/registrar.html')

        #Verifica si el nombre de usuario es unico
        if User.objects.filter(username=usuario).exists():
            messages.error(request, "El nombre de usuario ya se encuentra registrado")
            return render(request, 'gestion_de_usuarios/registrar.html')         

        # Verificar que sea mayor de dad
        if edad>= 18:
            # Crear un nuevo usuario en el sistema
            nuevo_usuario = User.objects.create_user(username=usuario, email=email, password=contrasenia, first_name=nombre, last_name=apellido)
            # Crear un perfil de cliente asociado al nuevo usuario
            perfil_cliente = PerfilCliente(user=nuevo_usuario, ciudad=ciudad, edad=edad)
            perfil_cliente.save()
            messages.success(request, "Se registro el usuario")
            
            # Autenticar al usuario recién creado
            user = authenticate(username=usuario,password=contrasenia)
            login(request, user)
            return redirect("homepage")
        else:
           messages.error(request, "Debe ser mayor de edad para registrarse en este sitio")
           return render(request, 'gestion_de_usuarios/registrar.html')
    return render(request, "/")

@authenticated_user
def ver_perfil(request, username=None):
    current_user = request.user
    perfil = None
    # Verificar si el usuario actual es un cliente
    if hasattr(current_user, 'perfilcliente'):
        perfil = current_user.perfilcliente
        template_name = "gestion_de_usuarios/ver_perfil_cliente.html"
    # Verificar si el usuario actual es un superusuario
    elif current_user.is_superuser:
        template_name = "gestion_de_usuarios/ver_perfil_admin.html"
    #no me toma la verificacion del staff ni por perfil empleado, el else funciona pero medio medio jaja
    elif hasattr(current_user, 'perfilempleado'):
        perfil = current_user.perfilempleado
        template_name = "gestion_de_usuarios/ver_perfil_empleado.html"

    return render(request, template_name, {'perfil': perfil})

@clienteOEmpleado
def modificar_perfil(request, username=None):
    current_user = request.user
    perfil = PerfilCliente.objects.get(user=current_user)
    if request.method == 'POST':
        form = FormularioModificarCliente(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Se guardaron los cambios con éxito!")
            return render(request, "gestion_de_usuarios/ver_perfil_cliente.html", {'perfil': perfil})
    else:
        form = FormularioModificarCliente(instance=perfil)
    return render(request, "gestion_de_usuarios/modificar_perfil.html", {'form': form, 'perfil': perfil, 'user_form': UserForm})
