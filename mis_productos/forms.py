from django import forms
from django.forms import ModelForm
from .models import Producto


class ProductoForm(ModelForm):
    class Meta():
        model = Producto
        fields = ("nombre", "estado", "categoria", "horario_disponibilidad", "sucursal", "imagen_principal", "imagen_extra1", "imagen_extra2", "imagen_extra3")
        labels = {
            "nombre": "",
            "estado" : "",
            "categoria" : "",
            "horario_disponibilidad" : "",
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
            "horario_disponibilidad": forms.TextInput(attrs={"class": "form-control", "placeholder": "Tu horario de disponibilidad"}),
            "sucursal": forms.TextInput(attrs={"class": "form-control", "placeholder": "Sucursal"}),
        }   