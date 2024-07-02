from django import forms
from django.forms import ModelForm
from .models import Servicio
from .models import ConfiguracionServicio

class ConfiguracionServicioForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionServicio
        fields = ['costo_publicacion', 'duracion_publicacion_dias']

        
class ServicioForm(ModelForm):
    class Meta():
        model = Servicio
        fields = ("ciudad", "imagen", "descripcion")
        labels = {
            "ciudad" : "",
            "imagen": "",
            "descripcion": "",
        }
        
        widgets = {
            "ciudad": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ciudad del servicio"}),
            "imagen": forms.FileInput(attrs={"class": "form-control", "placeholder": "Flyer del servicio"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "placeholder": "Descripcion del servicio"}),
        }   