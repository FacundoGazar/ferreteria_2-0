from django import forms
from django.forms import ModelForm
from .models import Servicio

class ServicioForm(ModelForm):
    class Meta():
        model = Servicio
        fields = ("sucursal", "imagen", "descripcion")
        labels = {
            "sucursal" : "",
            "imagen": "",
            "descripcion": "",
        }
        
        widgets = {
            "sucursal": forms.Select(attrs={"class": "form-select", "placeholder": "Sucursal donde publicaras tu servicio"}),
            "imagen": forms.FileInput(attrs={"class": "form-control", "placeholder": "Flyer del servicio"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "placeholder": "Descripcion del servicio"}),
        }   