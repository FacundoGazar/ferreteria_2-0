from django.urls import path
from . import views

urlpatterns = [
   # path("", views.homepage_view, name='homepage'),
    path("", views.tu_vista, name='homepage'),
]
