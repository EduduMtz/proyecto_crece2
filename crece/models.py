from django.db import models

class Peticion(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre
