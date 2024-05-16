from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . import unauthenticated_user, authenticated_user
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy


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


class ModificarContrasenaView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('modificar_contrasena_exitoso')


@authenticated_user
def modificar_contrasena_exitoso(request):
    return render(request, "authenticate/modificar_contrasena_exitoso.html")