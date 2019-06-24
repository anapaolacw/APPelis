from django.db import models
# Create your models here.
class Usuario (models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField(max_length=70)
    contrasena = models.CharField(max_length=50)
	
class Pelicula (models.Model):
	titulo = models.CharField(max_length=50)
	sinopsis = models.TextField(null = True)
	poster = models.ImageField(null = True)
	fechaEstreno = models.DateTimeField(null = True, auto_now_add=True)
	
class Resena (models.Model):
    resena = models.TextField(default='0')
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    idPelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)