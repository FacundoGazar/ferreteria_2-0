from django.urls import path
from .views import *

urlpatterns = [
    path("", mis_servicios_view, name='mis_servicios'),
    path("listar_solicitudes/", listar_solicitudes_view, name='listar_solicitudes'),
    path("solicitar_servicio/", solicitar_servicio_view, name='solicitar_servicio'),
    path("listar_solicitudes/<slug:slug>/", ver_imagen_view, name='ver_imagen'),
    path("listar_solicitudes/pagar/<slug:slug>/", pagar_publicacion_view, name='pagar_publicacion'),
]