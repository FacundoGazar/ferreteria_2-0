from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . import unauthenticated_user, authenticated_user
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.

@unauthenticated_user
def iniciar_sesion_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("homepage")
        else:
            messages.success(request, ("Los datos ingresados son invalidos, intente nuevamente..."))
            return redirect("iniciar_sesion")
    else:
        return render(request, "authenticate/login.html", {})

def cerrar_sesion_view(request):
    logout(request)
    messages.success(request, ("¡Cerraste sesión!"))
    return redirect("homepage")

@authenticated_user
def modificar_constrasena_view(request):
    if request.method == "POST":
        fm=PasswordChangeForm(user=request.user, data=request.POST)
        if fm.is_valid():
            messages.success(request, "Tu contrasena fue modificada correctamente.")
            return redirect("/")
    else:
        fm=PasswordChangeForm(user=request.user)
    return render (request, "authenticate/modificar_contrasena.html", {"fm":fm})