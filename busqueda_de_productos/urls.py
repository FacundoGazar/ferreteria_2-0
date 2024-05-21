from django.urls import path
from django.contrib.auth import views as auth_views
from buscar_productos import views

urlpatterns = [
    path('busqueda_de_productos/', views.buscar_productos, name='buscar_productos'),
]