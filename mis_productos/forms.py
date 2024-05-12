from django import forms
from django.forms import ModelForm
from .models import Producto


class ProductoForm(ModelForm):
    class Meta():
        model = Producto
        fields = ("nombre", "estado", "categoria", "dias", "horario_inicio", "horario_fin", "sucursal", "imagen_principal", "imagen_extra1", "imagen_extra2", "imagen_extra3")
        labels = {
            "nombre": "",
            "estado" : "",
            "categoria" : "",
            "dias" : "",
            "horario_inicio" : "",
            "horario_fin" : "",
            "sucursal" : "",
            "imagen_principal": "",
            "imagen_extra1" : "",
            "imagen_extra2" : "",
            "imagen_extra3" : "",
        }
        
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del producto"}),
            "estado": forms.TextInput(attrs={"class": "form-control", "placeholder": "Estado del producto"}),
            "categoria": forms.TextInput(attrs={"class": "form-control", "placeholder": "Categoria del producto"}),
            "dias": forms.TextInput(attrs={"class": "form-control", "placeholder": "Tus días disponibles de la semana"}),
            "horario_inicio": forms.TextInput(attrs={"class": "form-control", "placeholder": "Tu horario inicial de disponibilidad"}),
            "horario_fin": forms.TextInput(attrs={"class": "form-control", "placeholder": "Tu horario final de disponibilidad"}),
            "sucursal": forms.TextInput(attrs={"class": "form-control", "placeholder": "Sucursal"}),
        }   