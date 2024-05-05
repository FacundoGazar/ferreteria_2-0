from django.urls import path
from .views import *

urlpatterns = [
    path("", gestion_de_sucursales_view, name='gestion_de_sucursales'),
    path("agregar_sucursal/", agregar_sucursal_view, name='agregar_sucursal'),
    path("listar_sucursales/", listar_sucursales_view, name='listar_sucursales'),
    path("eliminar_sucursal/", eliminar_sucursal_view, name='eliminar_sucursal'),
    path("eliminar_sucursal/delete_sucursal/", delete_sucursal_view, name='delete_sucursal'),
    path("gestion_de_empleados/", gestion_de_empleados_view, name='gestion_de_empleados'),
    path("dar_de_baja/", dar_de_baja_view, name='dar_de_baja'),
    path("agregar_empleado/", agregar_empleado_view, name='agregar_empleado'),
]
