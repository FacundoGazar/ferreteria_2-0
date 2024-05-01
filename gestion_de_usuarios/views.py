from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from gestion_de_usuarios.models import PerfilCliente

def registrar(request):
    return render(request, 'gestion_de_usuarios/registrar.html')


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

        if User.objects.filter(usuario=usuario).exists():
            return render(request, 'gestion_de_usuarios/registrar.html', {'error_message': 'El nombre de usuario ya está en uso'})
        
        # Verificar que las contraseñas coincidan
        if edad >= 18:
            # Crear un nuevo usuario
            usuario = User.objects.create_user(usuario=usuario, nombre=nombre, apellido = apellido, email = email, contrasenia= contrasenia, ciduad = ciudad, edad= edad)
            
            # Crear una instancia del perfil de usuario y guardar los datos en la base de datos
            perfil_usuario = PerfilCliente(usuario=usuario, nombre=nombre, apellido = apellido, email = email, contrasenia= contrasenia, ciduad = ciudad, edad= edad)
            perfil_usuario.save()
            
            # Autenticar al usuario recién creado
            user = authenticate(usuario=usuario,contrasenia=contrasenia)
            login(request, usuario)
            return redirect('homepage')
        else:
           return render(request, 'gestion_de_usuarios/registrar.html', {'error_message': 'Debe ser mayor de edad para poder registrarse'})
    return render(request, 'gestion_de_usuarios/registrar.html')
