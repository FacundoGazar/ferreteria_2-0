from django.shortcuts import render

def buscar_productos(request):
    queryset = Productos.objects.all()
    
    context = {
        "lista": queryset
    }
    return render(request, "busqueda_de_productos/buscar_productos.html", context)