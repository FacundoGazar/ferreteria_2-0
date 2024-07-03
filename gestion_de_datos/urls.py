from django.urls import path
from .views import *

urlpatterns = [
    path("", gestion_de_datos_view, name='gestion_de_datos'),
    path("intercambios_por_sucursal/", estadisticas_intercambios_view, name='intercambios_por_sucursal'),
    path("intercambios_por_fecha/", estadisticas_intercambios_por_fecha_view, name='intercambios_por_fecha'),
    path("intercambios_sucursal_fecha/", estadisticas_intercambios_sucursal_fecha_view, name='intercambios_sucursal_fecha'),
    path("servicios_tiempo/", servicios_tiempo_view, name='servicios_tiempo'),
    path("servicios_ciudad/", servicios_ciudad_view, name='servicios_ciudad'),
    path("servicios_ciudad_tiempo/", servicios_ciudad_tiempo_view, name='servicios_ciudad_tiempo'),
    path("estadisticas_generales/", estadisticas_generales_view, name='estadisticas_generales'),
    path("intercambios_categoria/", estadisticas_intercambios_por_categoria_view, name='intercambios_categoria'),
    path("intercambios_categoria_sucursal/", estadisticas_intercambios_por_categoria_sucursal_view, name='intercambios_categoria_sucursal'),
    path('ingresos_por_sucursal/', ingresos_por_sucursal, name='ingresos_por_sucursal'),
    path('ingresos_por_tiempo/', ingresos_por_mes, name='ingresos_por_mes'),
    path('ventas_por_sucursal/', ventas_por_sucursal, name='ventas_por_sucursal'),
    path('ventas_por_tiempo/', ventas_por_mes, name='ventas_por_tiempo'),
    path('ingresos_por_sucursal_tiempo/', ingresos_por_sucursal_tiempo, name='ingresos_por_sucursal_tiempo'),
    path('productos_mas_vendidos/', productos_mas_vendidos, name='productos_mas_vendidos'),
    path('relacion_intercambio_venta/', relacion_intercambio_venta, name='relacion_intercambio_venta'),
]