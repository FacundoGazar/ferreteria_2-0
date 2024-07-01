# forms.py

from django import forms
from .models import ProductoCatalogo

class ProductoForm(forms.ModelForm):
    class Meta:
        model = ProductoCatalogo
        fields = ['descripcion', 'imagen_principal', 'imagen_extra1', 'imagen_extra2', 'imagen_extra3']
