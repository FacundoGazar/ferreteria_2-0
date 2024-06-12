from django import forms
from django.forms import ModelForm
from .models import Servicio


class ServicioForm(ModelForm):
    class Meta():
        model = Servicio
        fields = ("sucursal", "imagen")
        labels = {
            "sucursal" : "",
            "imagen": "",
        }
        
        widgets = {
            "sucursal": forms.Select(attrs={"class": "form-select", "placeholder": "Sucursal donde publicaras tu servicio"}),
        }   