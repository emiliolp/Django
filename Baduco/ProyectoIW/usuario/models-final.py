from django.db import models
from django.utils.encoding import smart_unicode

ABREVIATURAS1 = (
	('HOMBRE', 'HOMBRE'),
	('MUJER', 'MUJER'),

)

ABREVIATURAS2 = (
	('HOMOSEXUAL','HOMOSEXUAL'),
	('HETEROSEXUAL','HETEROSEXUAL'),
	('BISEXUAL','BISEXUAL'),
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

ABREVIATURAS6= (
	('PUBLICO', 'PUBLICO'),
	('PRIVADO', 'PRIVADO'),
	

)

ABREVIATURAS7= (
	('Verdadero','Verdadero'),
	('Falso','Falso'),
)




class PerfilUsuario(models.Model):

	nombre= models.CharField (max_length=30, unique=True)
	edad= models.IntegerField (range(18,200))
	sexo= models.CharField (max_length=10,choices=ABREVIATURAS1)
	localidad= models.CharField (max_length= 30)
	orientacionSexual= models.CharField (max_length=20,choices=ABREVIATURAS2)
	profesion= models.CharField (max_length=30)
	estudios= models.CharField (max_length=20,choices=ABREVIATURAS3)
	relaciones= models.CharField (max_length=30,choices=ABREVIATURAS4)
	creenciasReligiosas= models.CharField (max_length=20,choices=ABREVIATURAS5)
	intereses=models.CharField(max_length=100)
	informacionAdicional= models.CharField(max_length=100, help_text="Informacion adicional sobre el usuario")
	amigos= models.ManyToManyField (default='None', related_name="Amigo")

	def __unicode__ (self):
		return self.nombre

class Usuario(models.Model):
	nombre_usuario=models.CharField(max_length=30,unique=True)	
	perfilReal=models.OneToOneField(PerfilReal,related_name='usuario_PerfilReal')
	perfilFalso=models.OneToOneField(PerfilFalso,related_name='usuario_PerfilFalso')

	def __unicode__(self):
		return self.nombre_usuario
	
class PerfilReal(Usuario):

	tipo= models.CharField (default='Verdadero')
	def __unicode__ (self):
		return self.nombre

class PerfilFalso(Usuario):

	tipo= models.CharField (default= 'Falso')
	def __unicode__ (self):
		return self.nombre

class Comentario (models.Model):
	autor=models.ForeignKey(Usuario, related_name='usuario_autor')
	fecha=models.DateField()
	hora=models.TimeField()
	titulo=models.CharField()
	tipo=models.CharField(C)

class Votos (models.Model):
	usuario=OneToOneField(Usuario,related_name='usuario_voto')
	puntuacion=models.IntegerField(range(1,10))
		
		
	
	
	
	
	
