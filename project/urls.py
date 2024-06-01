"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("iniciar_sesion/", include("django.contrib.auth.urls")),
    path("iniciar_sesion/", include("iniciar_sesion.urls")),
    path("gestion_de_sucursales/", include("gestion_de_sucursales.urls")),
    path("gestion_de_usuarios/", include("gestion_de_usuarios.urls")),
    path("mis_productos/", include("mis_productos.urls")),
    path("busqueda_de_productos/", include("busqueda_de_productos.urls")),
    path("intercambiar_producto/", include("intercambiar_producto.urls")),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
