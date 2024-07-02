from django.urls import path
from .views import *

urlpatterns = [
    path("<slug:slug_intercambio>/", intercambiar_listar_mis_productos_view, name='intercambio listado'),
    path("<slug:slug_intercambio>/realizar_intercambio", realizar_intercambio_view, name='realizar intercambio'),
    path("ver_intercambios", ver_intercambios, name='ver_intercambios'),
    path('ver_detalle/<int:solicitud_id>/', detalle_intercambio, name='ver_detalle'),
    path('intercambios_por_sucursal_emp', intercambios_por_sucursal_view, name='intercambios_por_sucursal_emp'),
    path('confirmar_intercambio/<int:intercambio_id>/', confirmar_intercambio_view, name='confirmar_intercambio'),
    path('ausente_intercambio/<int:intercambio_id>/', ausente_intercambio_view, name='ausente_intercambio'),
    path('sin_venta/<int:intercambio_id>/', sin_venta_view, name='sin_venta'),
    path('registrar_venta/<int:intercambio_id>/', registrar_venta_view, name='registrar_venta'),
    path('marcar_venta/<int:intercambio_id>/', marcar_venta_view, name='marcar_venta'),
]
