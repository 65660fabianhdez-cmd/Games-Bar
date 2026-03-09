from django.db import models


class usuario(models.Model):
    nUsuario = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=10)

    def __str__(self):
        return self.nUsuario
