from django import forms
from django.contrib.auth.models import User
from gestion_de_usuarios.models import PerfilCliente
from django.contrib import messages

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','first_name', 'last_name']
        widgets = {
            'email': forms.TextInput(attrs={}),
            'first_name': forms.TextInput(attrs={}),
            'last_name': forms.TextInput(attrs={}),
        }

class FormularioModificarCliente(forms.ModelForm):
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")
    edad = forms.IntegerField(label="Edad", min_value=18,max_value=100)
    ciudad = forms.CharField(label="Ciudad")

    class Meta:
        model = PerfilCliente
        fields = ['edad', 'ciudad']

    def __init__(self, *args, **kwargs):
        super(FormularioModificarCliente, self).__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            user = self.instance.user
            self.fields['email'] = forms.EmailField(label="Email", initial=user.email, required=True)
            self.fields['first_name'] = forms.CharField(label="Nombre", initial=user.first_name, required=True)
            self.fields['last_name'] = forms.CharField(label="Apellido", initial=user.last_name, required=True)
        self.user_form = UserForm(*args, **kwargs)  # Inicializa el UserForm con los mismos argumentos

    def is_valid(self):
        # Combina la validación de ambos formularios
        return super(FormularioModificarCliente, self).is_valid() and self.user_form.is_valid()

    def save(self, commit=True):
        perfil = super(FormularioModificarCliente, self).save(commit=False)
        if commit:
            perfil.save()
        if perfil.user:
            user = perfil.user
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            if commit:
                user.save()
        return perfil

    def clean(self):
        cleaned_data = super(FormularioModificarCliente, self).clean()
        # No actualices los datos del usuario aquí
        return cleaned_data

