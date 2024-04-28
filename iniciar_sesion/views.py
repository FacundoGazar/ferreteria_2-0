from django.shortcuts import render

# Create your views here.

def iniciar_sesion_view(request):
    return render(request, "iniciar_sesion/iniciar_sesion_document.html")

def testeando(request):
    return render(request, "iniciar_sesion/testin.html")