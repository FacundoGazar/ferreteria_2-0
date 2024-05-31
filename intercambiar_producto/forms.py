from django import forms
from .models import Intercambio
from mis_productos.models import Producto
import datetime

class IntercambioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        producto_receptor = kwargs.pop('producto_receptor', None)  # Extrae 'producto_receptor' del kwargs
        horario_choices = kwargs.pop('horario_choices', [])
        super().__init__(*args, **kwargs)
        self.fields['horario'] = forms.ChoiceField(choices=horario_choices)
        if producto_receptor and producto_receptor.dias:  # Verifica si 'producto_receptor' existe y tiene días
            self.fields['dia'].widget = forms.Select(choices=[(dia, dia) for dia in producto_receptor.dias])

    class Meta:
        model = Intercambio
        exclude = ['producto_solicitante', 'producto_receptor', 'cliente_solicitante', 'cliente_receptor', 'estado']
        fields = ['dia', 'fecha', 'horario']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        dia = cleaned_data.get('dia')
        fecha = cleaned_data.get('fecha')
        print(f"Dia: {dia}, Fecha: {fecha}")

        # Accede a 'dia' desde 'producto_receptor'
        if self.producto_receptor:
            dia = self.producto_receptor.dias

        if fecha:
            hoy = datetime.date.today()
            if fecha <= hoy:
                raise forms.ValidationError("La fecha seleccionada debe ser posterior al día de hoy.")

        if dia and fecha:
            dia_semana = fecha.strftime('%A')
            dias_mapping = {
                'Lunes': 'Monday',
                'Martes': 'Tuesday',
                'Miercoles': 'Wednesday',
                'Jueves': 'Thursday',
                'Viernes': 'Friday',
            }

            if dias_mapping[dia] != dia_semana:
                raise forms.ValidationError(f"La fecha seleccionada no corresponde al día {dia}. Por favor, selecciona una fecha que sea un {dia}.")
            return cleaned_data