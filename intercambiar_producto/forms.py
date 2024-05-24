from django import forms
from .models import Intercambio

class IntercambioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        horario_choices = kwargs.pop('horario_choices', [])
        super().__init__(*args, **kwargs)
        self.fields['horario'] = forms.ChoiceField(choices=horario_choices)
    
    class Meta:
        model = Intercambio
        exclude = ['producto_solicitante', 'producto_receptor', 'cliente_solicitante', 'cliente_receptor', 'estado', 'dia']
