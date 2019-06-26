from django.db import models
class Pelicula (models.Model):
	poster = models.ImageField(null = True)
	