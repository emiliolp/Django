from django.db import models
from django.utils.encoding import smart_unicode
from django.contrib.auth.models import User

ABREVIATURAS1 = (
	('Hombre', 'Hombre'),
	('Mujer', 'Mujer'),

)

ABREVIATURAS2 = (
	('Heterosexual','Heterosexual'),
	('Homosexual','Homosexual'),
	('Bisexual','Bisexual'),
)

ABREVIATURAS3 = (
	('ESO','Educacion Secundaria'),
	('Bachiller','Bachiller'),
	('Estudios Universitarios','Estudios Universitarios'),
	('Sin Estudios', 'Sin Estudios'),
	('Otros', 'Otros'),

)

ABREVIATURAS4 = (
	('Sin Pareja', 'Sin Pareja'),
	('Con Pareja', 'Con Pareja'),
	('Con rollo', 'Con rollo'),
	('Busco amistad', 'Busco amistad'),
	('Busco pareja', 'Busco pareja'),
	('Busco rollo', 'Busco rollo'),

)

ABREVIATURAS5 = (
	('Ateo', 'Ateo'),
	('Agnostico', 'Agnostico'),
	('Cristiano', 'Cristiano'),
	('Musulman', 'Musulman'),
	('Judio', 'Judio'),
	('Budista', 'Budista'),
	('Otra' , 'Otra'),

)

ABREVIATURAS6=(
	('Real','Real'),
	('Falso','Falso'),
)

RANGO_VOTOS = [(i,i) for i in range (11)]

class Usuario (User):
	perfilReal = models.OneToOneField ('PerfilUsuario', default = None, related_name='usuario_PerfilReal')
	perfilFalso = models.OneToOneField ('PerfilUsuario', default = None, related_name='usuario_PerfilFalso')
	perfilActivo = models.CharField (max_length=20, default = 'Real', choices = ABREVIATURAS6)

	def __unicode__(self):
		return self.username


class PerfilUsuario (models.Model):
	nombre = models.CharField (max_length=30, unique=True, blank = True, null = True)
	edad = models.IntegerField (range(18,200), blank = True, null = True)
	sexo = models.CharField (max_length=50, blank = True, null = True, choices=ABREVIATURAS1)
	localidad = models.CharField (max_length= 50, blank = True, null = True)
	orientacionSexual = models.CharField (max_length=20, blank = True, null = True, choices=ABREVIATURAS2)
	profesion = models.CharField (max_length=50, blank = True, null = True)
	estudios = models.CharField (max_length=50, blank = True, null = True, choices=ABREVIATURAS3)
	relaciones = models.CharField (max_length=50, blank = True, null = True, choices=ABREVIATURAS4)
	creenciasReligiosas = models.CharField (max_length=50, blank = True, null = True, choices=ABREVIATURAS5)
	intereses = models.CharField(max_length=100, blank = True, null = True)
	informacionAdicional = models.TextField (blank = True, null = True, help_text="Informacion adicional sobre el usuario")
	amigos = models.ManyToManyField ('PerfilUsuario', default='None', related_name = "PerfilAmigo_PerfilUsuario")
	imagen = models.ImageField (upload_to = 'usuario', verbose_name = 'ImagenPerfil')
	# Indica si es el perfil real o el falso
	tipo = models.CharField (max_length = 30)
	latitud=models.FloatField(null=True,blank=True,default=0)
	longitud=models.FloatField(null=True,blank=True,default=0)
	mediaVotos=models.FloatField(null=True,blank=True,default=0)

	def __unicode__ (self):
		return self.nombre

class PeticionAmistad (models.Model):
	perfil_solicitante = models.CharField (max_length = 30, blank = True, null = True)
	fecha = models.DateField (default = None, blank = True, null = True)
	comentario = models.TextField (blank = True, null = True)
	perfil_objetivo = models.ForeignKey ('PerfilUsuario', default = 'None', blank = True, null = True, related_name = "PeticionAmistad_PerfilUsuairo")

	def __unicode__ (self):
		return self.usuario_solicitante

class Comentario (models.Model):
	perfilReceptor = models.ForeignKey ('PerfilUsuario', related_name = 'Comentario_PerfilUsuario')
	perfilEmisor = models.CharField (max_length = 50, blank = True, null = True)
	fecha = models.DateField (default = None, blank = True, null = True)
	hora = models.TimeField (default = None, blank = True, null = True)
	texto = models.TextField (default = None, blank = True, null = True)
	comentario = models.ManyToManyField ('Comentario', default = 'None', related_name = "Comentario_Comentario")
	padre = models.CharField (max_length = 10)

	def __unicode__ (self):
		return self.perfilEmisor

class Voto (models.Model):
	perfilVotado = models.ForeignKey ('PerfilUsuario', related_name = 'Voto_PerfilUsuario')
	puntuacion = models.IntegerField (choices = RANGO_VOTOS, blank = True, null = True)
	perfilVotante = models.CharField (max_length = 50, blank = True, null = True)
	hora = models.TimeField (default = None, blank = True, null = True)
	texto = models.TextField (default = None, blank = True, null = True)

	def __unicode__ (self):
			return self.perfilVotante
