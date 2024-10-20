from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Carreras(models.Model):
    carrera = models.CharField(max_length=300)

    def __str__(self):
        return self.carrera
    
class Estudiantes(models.Model):
    nombre = models.CharField(max_length=300)
    apellido = models.CharField(max_length=300)
    carrera_on = models.ForeignKey(Carreras, on_delete=models.CASCADE, blank=True, null=True, related_name="carreraOn")
    carnet = models.CharField(max_length=12)

    def __str__(self):
        return self.Nombre
