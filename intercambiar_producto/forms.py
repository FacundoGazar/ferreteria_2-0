from django import forms
from .models import Intercambio
import datetime

class IntercambioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.producto_receptor = kwargs.pop('producto_receptor', None)
        horario_choices = kwargs.pop('horario_choices', [])
        super().__init__(*args, **kwargs)
        self.fields['horario'] = forms.ChoiceField(choices=horario_choices)
        if self.producto_receptor and self.producto_receptor.dias: 
            self.fields['dia'].widget = forms.Select(choices=[(dia, dia) for dia in self.producto_receptor.dias])
        if horario_choices:
            self.fields['horario'] = forms.ChoiceField(choices=horario_choices)
        

    class Meta:
        model = Intercambio
        exclude = ['producto_solicitante', 'producto_receptor', 'cliente_solicitante', 'cliente_receptor', 'estado']
        fields = ['dia', 'fecha', 'horario','producto_receptor']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        dia = cleaned_data.get('dia')
        fecha = cleaned_data.get('fecha')
        producto_receptor = cleaned_data.get("producto_receptor")
        
        if self.producto_receptor:
            dia = self.producto_receptor.dias
        else:
            dia = producto_receptor.dias
        if fecha:
            hoy = datetime.date.today()
            if fecha <= hoy:
                raise forms.ValidationError("La fecha seleccionada debe ser posterior al día de hoy.")

        dias_mapping = {
            'Lunes': 'Monday',
            'Martes': 'Tuesday',
            'Miércoles': 'Wednesday',
            'Jueves': 'Thursday',
            'Viernes': 'Friday',
            'Sábado': 'Saturday',
            'Domingo': 'Sunday'
        }

        if not self.producto_receptor:
            raise forms.ValidationError("Producto receptor no definido.")
        
        dia = self.producto_receptor.dias
        fecha = cleaned_data.get('fecha')
        
        if fecha:
            dia_semana = fecha.strftime('%A') 
            dia_semana = dia_semana.capitalize() 

            if dia not in dias_mapping:
                raise forms.ValidationError(f"Día '{dia}' no está en el mapeo de días.")

            if dias_mapping[dia] != dia_semana:
                raise forms.ValidationError("La fecha seleccionada no coincide con el día de semana disponible.")
        return cleaned_data