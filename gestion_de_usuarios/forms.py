from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

"""#formulario que tiene django
class CustomUserCreationForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ['Usuario', 'Nombre', 'Apellido', 'email', 'Contraseña', 'Ciudad', 'Edad']
	def clean_usuario(self):
		usuario = self.cleaned_data['usuario']

		if User.objects.filter(usuario=usuario).exists():
			raise forms.ValidationError('Este usuario ya está registrado')
		
		return usuario"""