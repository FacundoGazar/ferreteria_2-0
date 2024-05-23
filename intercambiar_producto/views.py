from django.shortcuts import render
from mis_productos.models import Producto
from iniciar_sesion import soy_cliente
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Intercambio
from .forms import IntercambioForm

@soy_cliente
def intercambiar_listar_mis_productos_view(request, slug_intercambio):
    usuario = request.user
    queryset = Producto.objects.filter(cliente=usuario)

    context = {
        "lista": queryset,
        "slug_intercambio": slug_intercambio,
    }
    
    return render(request, "intercambiar_producto/intercambiar_listado.html", context)

@soy_cliente
def realizar_intercambio_view(request, slug_intercambio):
    producto_solicitante = Producto.objects.get(cliente=request.user)
    producto_receptor = Producto.objects.get(slug=slug_intercambio)
    
    if request.method == 'POST':
        form = IntercambioForm(request.POST)
        if form.is_valid():
            Intercambio = form.save(commit=False)
            # Asignar los valores de producto_solicitante, cliente_solicitante, producto_receptor y cliente_receptor directamente
            Intercambio.producto_solicitante = producto_solicitante
            Intercambio.cliente_solicitante = request.user
            Intercambio.producto_receptor = producto_receptor
            Intercambio.cliente_receptor = producto_receptor.cliente
            Intercambio.estado = form.cleaned_data['estado']
            Intercambio.save()
            messages.success(request, "Solicitud de intercambio enviada con éxito.")
            return redirect('homepage')
        else:
            print(form.errors)
            messages.error(request, "Por favor, verifica el formulario.")
    else:
        form = IntercambioForm()

    return render(request, 'intercambiar_producto/realizar_intercambio.html', {'form': form, 'producto_solicitante': producto_solicitante, 'producto_receptor': producto_receptor})