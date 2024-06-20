from django.urls import path
from catalogo import views

urlpatterns = [
    path("subir_producto_catalogo/", views.subir_producto, name='subir_producto_catalogo'),
    path("listar_catalogo/", views.ver_catalogo, name='listar_catalogo'),
    path("historial_productos/", views.ver_historial, name='ver_historial'),
    path("eliminar_producto/<slug:slug>/", views.eliminar_producto, name='eliminar_producto'),
    path("restaurar_producto/<slug:slug>/", views.restaurar_producto, name='restaurar_producto'),
    path('editar_producto/<slug:slug>/', views.editar_producto, name='editar_producto'),
]