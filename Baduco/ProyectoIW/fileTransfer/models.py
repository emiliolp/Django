from django.db import models

class files(models.Model):
	docfile = models.FileField(upload_to='documents/%Y/%m/%d')