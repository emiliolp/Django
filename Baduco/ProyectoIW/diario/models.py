from django.db import models
from usuario.models import Usuario,PerfilUsuario

class Agenda (models.Model):

	nombre = models.CharField (max_length = 30)
	usuario = models.OneToOneField (Usuario, related_name = "Agenda_Usuario")

	def __unicode__ (self):
		return self.nombre

class DiarioPersonal (models.Model):

	nombre = models.CharField (max_length = 30)
	usuario = models.OneToOneField (Usuario, related_name = "DiarioPersonal_Usuario")

	def __unicode__ (self):
		return self.usuario

class DiarioPensamientos (models.Model):

	nombre = models.CharField (max_length = 30)
	usuario = models.OneToOneField (Usuario, related_name = "DiarioPensamientos_Usuario")

	def __unicode__ (self):
		return self.perfilUsuario

class Entrada (models.Model):

	titulo = models.CharField (max_length = 50, default = None, blank = True, null = True)
	fecha = models.DateField (default = None, blank = True, null = True)
	hora = models.TimeField (default = None, blank = True, null = True)
	contenido = models.TextField (default = None, blank = True, null = True)


class EntradaAgenda (Entrada):

	agenda = models.ForeignKey ('Agenda', related_name = "EntradaAgenda_Agenda")

	def __unicode__ (self):
		return self.titulo

class EntradaDiarioPersonal (Entrada):

	diarioPersonal = models.ForeignKey ('DiarioPersonal', related_name = "EntradaDiarioPersonal_DiarioPersonal")

	def __unicode__ (self):
		return self.titulo

class EntradaDiarioPensamientos (Entrada):

	diarioPensamientos = models.ForeignKey ('DiarioPensamientos', related_name = "EntradaDiarioPensamientos_DiarioPensamientos")

	def __unicode__ (self):
		return self.titulo
