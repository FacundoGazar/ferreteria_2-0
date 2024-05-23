from django import forms
from .models import Intercambio

class IntercambioForm(forms.ModelForm):
    class Meta:
        model = Intercambio
        fields = ('producto_solicitante', 'producto_receptor', 'cliente_solicitante', 'cliente_receptor', 'estado')
        widgets = {
            'estado': forms.Select(choices=Intercambio.ESTADOS),
        }
