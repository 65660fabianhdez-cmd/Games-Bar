from django.db import models


class Sucursal(models.Model):

    nombre = models.CharField(max_length=100)

    direccion = models.CharField(max_length=150)

    ciudad = models.CharField(max_length=100)

    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    encargado = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    horario = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    ESTADO = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo')
    ]

    estado = models.CharField(
        max_length=10,
        choices=ESTADO,
        default='Activo'
    )

    def __str__(self):
        return self.nombre
