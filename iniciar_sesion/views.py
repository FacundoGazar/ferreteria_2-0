from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def iniciar_sesion_view(request):
    return render(request, "registration/login.html", {})

def cerrar_sesion_view(request):
    logout(request)
    return redirect("homepage")    