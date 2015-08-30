from django.db import models
from django.utils.encoding import smart_unicode
# Create your models here.

POSITION_CHOICES=(
	('POR','PORTERO'),
	('DEF','DEFENSA'),
	('MED','MEDIOCENTRO'),
	('DEL','DELANTERO'),
)

class Equipo(models.Model):
	nombre_equipo=models.CharField(max_length=30,unique=True)
	escudo = models.ImageField(upload_to='escudos', verbose_name='Foto del escudo', default='escudos/esc0.jpg')
	nombre_estadio=models.CharField(max_length=50)
	aforo=models.IntegerField()
	anyo_fundacion=models.IntegerField()
	ciudad=models.CharField(max_length=50)
	nombre_presidente=models.CharField(max_length=50,unique=True)
	nombre_entrenador=models.CharField(max_length=50,unique=True)
	numero_socios=models.IntegerField()
	puntos=models.IntegerField(default=0)
	partidos_jugados=models.IntegerField(default=0)
	partidos_ganados=models.IntegerField(default=0)
	partidos_empatados=models.IntegerField(default=0)
	partidos_perdidos=models.IntegerField(default=0)
	goles_favor=models.IntegerField(default=0)
	goles_contra=models.IntegerField(default=0)
	diferencia_goles=models.IntegerField(default=0)
	posicion=models.IntegerField(unique=True)

	def __unicode__ (self):
		return self.nombre_equipo

class Jugador(models.Model):
	nombre=models.CharField(max_length=30,unique=True)
	fecha_nacimiento=models.DateField()
	peso=models.IntegerField()
	estatura=models.DecimalField(max_digits=3,decimal_places=2)
	posicion=models.CharField(max_length=3,choices=POSITION_CHOICES)
	cara = models.ImageField(upload_to='faces', verbose_name='Foto del jugador', default='faces/desconocido.jpg')
	equipo=models.ForeignKey(Equipo,related_name='Equipo')
	goles=models.IntegerField()
	tarjetas_rojas=models.IntegerField()
	tarjetas_amarillas=models.IntegerField()
	sancionado=models.BooleanField()
	lesionado=models.BooleanField()

	def __unicode__ (self):
		return self.nombre

class Arbitro(models.Model):
	nombre=models.CharField(max_length=30,unique=True)
	cara = models.ImageField(upload_to='faces', verbose_name='Foto del arbitro', default='faces/desconocido.jpg')
	colegio_arbitral=models.CharField(max_length=30)
	numero_temporadas=models.IntegerField()

	def __unicode__ (self):
		return self.nombre

class Jornada(models.Model):
	numero=models.CharField(max_length=2,unique=True)
	fecha_inicio=models.DateField()
	terminada=models.BooleanField()

	def __unicode__ (self):
		return self.numero

class Partido(models.Model):
	nombre_equipo_casa=models.ForeignKey(Equipo,related_name='Equipo_Casa')
	nombre_equipo_fuera=models.ForeignKey(Equipo,related_name='Equipo_Fuera')
	resultado_equipo_casa=models.IntegerField(null = True, blank = True)
	resultado_equipo_fuera=models.IntegerField(null = True, blank = True)
	fecha_partido=models.DateField()
	jornada=models.ForeignKey(Jornada,related_name='Jornada')
	arbitro=models.ForeignKey(Arbitro,related_name='Arbitra')

	def __unicode__ (self):
		return '%s - %s' % (self.nombre_equipo_casa,self.nombre_equipo_fuera)


class Participa(models.Model):
	jugador=models.ForeignKey(Jugador,related_name='Jugador')
	partido=models.ForeignKey(Partido,related_name='Partido participa')
	amarilla=models.IntegerField()
	roja=models.IntegerField()
	minutos=models.IntegerField()
	goles=models.IntegerField()

	def __unicode__ (self):
		return '%s %s' % (self.jugador,self.partido)


	

