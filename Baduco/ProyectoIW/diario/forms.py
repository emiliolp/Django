#encoding: utf-8

from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from usuario.models import Usuario, PerfilUsuario
from diario.models import Agenda, DiarioPersonal, DiarioPensamientos, EntradaAgenda, EntradaDiarioPersonal, EntradaDiarioPensamientos

class EntradaAgendaForm (forms.ModelForm):
	class Meta:
		model = EntradaAgenda
		fields = ('titulo', 'contenido')

	def __init__(self, *args, **kwargs):
		super (EntradaAgendaForm, self).__init__(*args, **kwargs)
		self.fields ['titulo'].label = "Título"
		self.fields ['contenido'].label = "Contenido"

	def save (self, commit = True):
		entradaAgenda = super (EntradaAgendaForm, self).save (commit = False)
		if commit:
			entradaAgenda.hora = datetime.now ().strftime ("%H:%M")
			entradaAgenda.fecha = datetime.now ()
			entradaAgenda.save ()
		return entradaAgenda

class EntradaDiarioPersonalForm (forms.ModelForm):
	class Meta:
		model = EntradaDiarioPersonal
		fields = ('titulo', 'contenido')

	def __init__(self, *args, **kwargs):
		super (EntradaDiarioPersonalForm, self).__init__(*args, **kwargs)
		self.fields ['titulo'].label = "Título"
		self.fields ['contenido'].label = "Contenido"

	def save (self, commit = True):
		entradaPersonal = super (EntradaDiarioPersonalForm, self).save (commit = False)
		if commit:
			entradaPersonal.hora = datetime.now ().strftime ("%H:%M")
			entradaPersonal.fecha = datetime.now ()
			entradaPersonal.save ()
		return entradaPersonal

class EntradaDiarioPensamientosForm (forms.ModelForm):
	class Meta:
		model = EntradaDiarioPensamientos
		fields = ('titulo', 'contenido')

	def __init__(self, *args, **kwargs):
		super (EntradaDiarioPensamientosForm, self).__init__(*args, **kwargs)
		self.fields ['titulo'].label = "Título"
		self.fields ['contenido'].label = "Contenido"

	def save (self, commit = True):
		entradaPensamientos = super (EntradaDiarioPensamientosForm, self).save (commit = False)
		if commit:
			entradaPensamientos.hora = datetime.now ().strftime ("%H:%M")
			entradaPensamientos.fecha = datetime.now ()
			entradaPensamientos.save ()
		return entradaPensamientos
