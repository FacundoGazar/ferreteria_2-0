from django.shortcuts import render, redirect
from django.contrib import messages
from catalogo.models import ProductoCatalogo
from catalogo.forms import ProductoForm

def subir_producto(request):
    if request.method == 'POST':
        # Obtener los datos del formulario enviado por el usuario
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        imagen_principal = request.FILES.get('imagen_principal')
        imagen_extra1 = request.FILES.get('imagen_extra1')
        imagen_extra2 = request.FILES.get('imagen_extra2')
        imagen_extra3 = request.FILES.get('imagen_extra3')

        # Verificar si el nombre del producto ya existe
        if ProductoCatalogo.objects.filter(nombre=nombre).exists():
            messages.error(request, "El nombre del producto ya está registrado.")
            return render(request, 'catalogo/subir_producto_catalogo.html')

        # Crear una instancia de ProductoCatalogo con los datos del formulario
        producto_catalogo = ProductoCatalogo(
            nombre=nombre,
            descripcion=descripcion,
            # Guardar las imágenes en los campos correspondientes
            imagen_principal=imagen_principal,
            imagen_extra1=imagen_extra1,
            imagen_extra2=imagen_extra2,
            imagen_extra3=imagen_extra3
        )
        producto_catalogo.save()

        messages.success(request, "Producto registrado en el catálogo exitosamente.")
        return redirect('subir_producto_catalogo')  # Redirigir a la misma página para un nuevo formulario

    return render(request, "catalogo/subir_producto_catalogo.html")

def ver_catalogo(request):
    catalogo = ProductoCatalogo.objects.filter(visible=True)
    
    context = {
        'catalogo': catalogo,
    }
    return render(request, "catalogo/listar_catalogo.html", context)

def ver_historial(request):
    catalogo = ProductoCatalogo.objects.filter(visible=False)
    
    context = {
        'catalogo': catalogo,
    }
    return render(request, "catalogo/listar_catalogo.html", context)


def eliminar_producto(request, slug):
    producto = ProductoCatalogo.objects.get(slug=slug)
    producto.visible = False
    producto.save()
    return render(request, "catalogo/listar_catalogo.html", {'producto': producto})

def restaurar_producto(request, slug):
    producto = ProductoCatalogo.objects.get(slug=slug)
    producto.visible = True
    producto.save()
    return render(request, "catalogo/listar_catalogo.html", {'producto': producto})

def editar_producto(request, slug):
    producto = ProductoCatalogo.objects.get(slug=slug)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_catalogo')  # Redirigir a la página del catálogo después de guardar los cambios
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'catalogo/editar_producto.html', {'form': form, 'producto': producto})