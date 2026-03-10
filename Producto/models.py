from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Producto_gb(models.Model):

    nombre_producto = models.CharField(
        max_length=50
    )

    cantidad = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(9999)
        ]
    )

    unidad_medida = models.CharField(
        max_length=10,
        choices=[
            ('kg', 'kg'),
            ('pieza', 'pieza'),
            ('caja', 'caja'),   
            ('litro', 'litro')
        ]
    )

    proveedor = models.ForeignKey(
        'Proveedor.Proveedor_pxn',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.nombre_producto
