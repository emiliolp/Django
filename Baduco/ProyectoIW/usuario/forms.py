#encoding: utf-8

from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from usuario.models import Usuario, PerfilUsuario, PeticionAmistad, Comentario, Voto
from diario.models import Agenda, DiarioPersonal, DiarioPensamientos

class UserForm (forms.ModelForm):
	class Meta:
		model = Usuario
		fields = ('first_name', 'last_name', 'username', 'email',)

	password1 = forms.CharField (label = 'Contraseña', widget = forms.PasswordInput)
	password2 = forms.CharField (label = 'Confirmar contraseña', widget = forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		super (UserForm, self).__init__(*args, **kwargs)
		self.fields ['first_name'].label = "Nombre"
		self.fields ['last_name'].label = "Apellidos"
		self.fields ['username'].label = "Nombre de usuario"
		self.fields ['email'].label = "Email"

	# Comprueba si el nombre de usuario introducido ya existe
	def clean_username (self):
		username = self.cleaned_data ["username"]
		try:
			Usuario.objects.get (username = username)
		except Usuario.DoesNotExist:
			return username
		raise forms.ValidationError ("El nombre de usuario introducido ya existe.")

	# Comprueba que la contraseña introducida es correcta
	def clean_password2 (self):
		password1 = self.cleaned_data.get ("password1", "")
		password2 = self.cleaned_data ["password2"]
		if password1 != password2:
			raise forms.ValidationError ("La contraseña no coincide.")
		return password2

	def save (self, commit = True):
		user = super (UserForm, self).save (commit = False)
		user.set_password (self.cleaned_data ["password1"])
		user.is_staff = False
		user.is_superuser = False
		user.perfilReal = PerfilUsuario.objects.create (tipo = 'Real')
		user.perfilFalso = PerfilUsuario.objects.create (tipo = 'Falso')
		if commit:
			user.save ()
		return user

class PerfilForm (forms.ModelForm):

	class Meta:
		model = PerfilUsuario
		fields = ('nombre', 'edad', 'sexo', 'localidad', 'orientacionSexual', 'profesion', 'estudios', 'relaciones', 'creenciasReligiosas', 'intereses', 'informacionAdicional', 'imagen')

	def __init__(self, *args, **kwargs):
		super (PerfilForm, self).__init__(*args, **kwargs)
		self.fields ['nombre'].label = "Nombre"
		self.fields ['edad'].label = "Edad"
		self.fields ['sexo'].label = "Sexo"
		self.fields ['localidad'].label = "Localidad"
		self.fields ['orientacionSexual'].label = "Orientación sexual"
		self.fields ['profesion'].label = "Profesión"
		self.fields ['estudios'].label = "Estudios"
		self.fields ['relaciones'].label = "Relación sentimental"
		self.fields ['creenciasReligiosas'].label = "Creencias religiosas"
		self.fields ['intereses'].label = "Intereses personales"
		self.fields ['informacionAdicional'].label = "Información adicional"
		self.fields ['imagen'].label = "Imagen de perfil"

	def save (self, commit = True):
		perfil = super (PerfilForm, self).save (commit = False)
		if commit:
			perfil.save ()
		return perfil

class PeticionAmistadForm (forms.ModelForm):

	class Meta:
		model = PeticionAmistad
		fields = ('comentario',)

	def __init__(self, *args, **kwargs):
		super (PeticionAmistadForm, self).__init__(*args, **kwargs)
		self.fields ['comentario'].label = "Comentario"

	def save (self, commit = True):
		peticion = super (PeticionAmistadForm, self).save (commit = False)
		if commit:
			peticion.fecha = datetime.now ()
			peticion.save ()
		return peticion

class ComentarioForm (forms.ModelForm):

	class Meta:
		model = Comentario
		fields = ('texto',)

	def __init__(self, *args, **kwargs):
		super (ComentarioForm, self).__init__(*args, **kwargs)
		self.fields ['texto'].label = "Comentario"

	def save (self, commit = True):
		comentario = super (ComentarioForm, self).save (commit = False)
		if commit:
			comentario.fecha = datetime.now ()
			comentario.hora = datetime.now ().strftime ("%H:%M")
			comentario.save ()
		return comentario

class VotoForm (forms.ModelForm):

	class Meta:
		model = Voto
		fields = ('puntuacion',)

	def __init__(self, *args, **kwargs):
		super (VotoForm, self).__init__(*args, **kwargs)
		self.fields ['puntuacion'].label = "Puntuación"

	def save (self, commit = True):
		voto = super (VotoForm, self).save (commit = False)
		if commit:
			voto.fecha = datetime.now ()
			voto.hora = datetime.now ().strftime ("%H:%M")
			voto.save ()
		return voto
