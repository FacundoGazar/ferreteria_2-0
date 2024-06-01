from django.urls import path
from django.contrib.auth import views as auth_views
from busqueda_de_productos import views

urlpatterns = [
    path('buscar_productos', views.buscar_productos, name='buscar_productos'),
    path('ver_detalle_intercambio/<slug:slug>/', views.ver_detalle, name='ver_detalle_intercambio'),
]
