from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from gestion_de_usuarios.models import PerfilCliente
import tkinter as tk
from tkinter import messagebox

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

        if User.objects.filter(username=usuario).exists():
            return render(request, 'gestion_de_usuarios/registrar.html', {'error_message': 'El nombre de usuario ya está en uso'})
      
        # Verificar que sea mayor de dad
        if edad >= 18:
            # Crear un nuevo usuario en el sistema
            nuevo_usuario = User.objects.create_user(username=usuario, email=email, password=contrasenia, first_name=nombre, last_name=apellido)
            # Crear un perfil de cliente asociado al nuevo usuario
            perfil_cliente = PerfilCliente(user=nuevo_usuario, ciudad=ciudad, edad=edad)
            perfil_cliente.save()
            messagebox.showinfo("Se registro el usuario")
            
            # Autenticar al usuario recién creado
            user = authenticate(usuario=usuario,contrasenia=contrasenia)
            login(request, usuario)
            return redirect('homepage')
        else:
           return render(request, 'gestion_de_usuarios/registrar.html', {'error_message': 'Debe ser mayor de edad para poder registrarse'})

