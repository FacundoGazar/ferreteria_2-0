from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def iniciar_sesion_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("homepage")
        else:
            messages.success(request, ("Hubo un errror al iniciar sesión, intente nuevamente..."))
            return redirect("iniciar_sesion")
    else:
        return render(request, "authenticate/login.html", {})

def cerrar_sesion_view(request):
    logout(request)
    return redirect("homepage")