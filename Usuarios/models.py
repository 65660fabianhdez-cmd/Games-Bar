from django.db import models


class usuario(models.Model):
    ROLES = [
        ('operaciones', 'Operaciones'),
        ('proveedor', 'Proveedor'),
        ('analista_reportes', 'Analista Reportes'),
    ]

    nUsuario = models.CharField(max_length=50, unique=True)
    contrasena = models.CharField(max_length=10)
    rol = models.CharField(max_length=20, choices=ROLES, default='operaciones')

    def __str__(self):
        return f"{self.nUsuario} ({self.get_rol_display()})"
