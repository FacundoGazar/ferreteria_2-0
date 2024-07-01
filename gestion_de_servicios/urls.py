from django.urls import path
from .views import *

urlpatterns = [
    path("", mis_servicios_view, name='mis_servicios'),
    path("listar_solicitudes/", listar_solicitudes_view, name='listar_solicitudes'),
    path("solicitar_servicio/", subir_servicio_view, name='subir_servicio'),
    path("listar_solicitudes/<slug:slug>/", ver_imagen_view, name='ver_imagen'),
    path("listar_solicitudes/pagar/<slug:slug>/", pagar_publicacion_view, name='pagar_publicacion'),
    path("listar_solicitudes_clientes/", listar_solicitudes_clientes_view, name='listar_solicitudes_clientes'),
    path("listar_solicitudes_clientes/<slug:slug>/", evaluar_servicio_view, name='evaluar_servicio'),
    path("listar_solicitudes_clientes/<slug:slug>/motivo", mandar_motivo_view, name='mandar_motivo'),
    path('servicios_publicados', servicios_publicados_view, name='servicios_publicados'),
    path("historial_servicios/", ver_historial_view, name='ver_historial_servicios'),
    path("eliminar_servicio/<slug:slug>/", eliminar_servicio_view, name='eliminar_servicio'),
]
