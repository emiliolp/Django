from django.db import models
from django.utils.encoding import smart_unicode

# Create your models here.

class New(models.Model):
	titular=models.CharField(max_length=200)
	noticia = models.TextField()
	fecha = models.DateField()
	imagen = models.ImageField(upload_to='noticia', verbose_name='Foto de la noticia')
	def __unicode__(self):
		return self.titular
