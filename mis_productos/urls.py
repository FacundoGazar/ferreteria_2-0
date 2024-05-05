from django.urls import path
from .views import *


urlpatterns = [
    path("", mis_productos_view, name='mis_productos'),
    path("subir_producto/", subir_producto_view, name='subir_producto'),
    path("eliminar_producto/", eliminar_producto_view, name='eliminar_producto'),
    path("listar_mis_productos/<slug:slug>/", ver_detalle_view, name='ver_detalle'),
    path("listar_mis_productos/", listar_mis_productos_view, name='listar_mis_productos'),
]