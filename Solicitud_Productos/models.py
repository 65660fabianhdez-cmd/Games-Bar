from datetime import date

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class SolicitudProducto(models.Model):

    ESTADOS = [
        ("Pendiente", "Pendiente"),
        ("En proceso", "En proceso"),
        ("Completada", "Completada"),
        ("Cancelada", "Cancelada"),
    ]

    folio = models.CharField(
        max_length=25,
        unique=True,
        blank=True,
        null=True,
    )

    fecha = models.DateField(
        default=timezone.now
    )

    proveedor = models.ForeignKey(
        "Proveedor.Proveedor_pxn",
        on_delete=models.CASCADE,
        related_name="solicitudes_producto",
    )

    observaciones = models.TextField(
        blank=True
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="Pendiente",
    )

    class Meta:
        ordering = ["-fecha", "-id"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.folio:
            fecha_folio = self.fecha

            if isinstance(fecha_folio, str):
                fecha_folio = date.fromisoformat(fecha_folio)

            folio = f"SOL-{fecha_folio.strftime('%Y%m%d')}-{self.pk:04d}"
            SolicitudProducto.objects.filter(pk=self.pk).update(folio=folio)
            self.folio = folio

    def __str__(self):
        return self.folio or f"Solicitud #{self.pk}"


class DetalleSolicitudProducto(models.Model):

    CATEGORIAS = [
        ("Videojuego", "Videojuego"),
        ("Consola", "Consola"),
        ("Control", "Control"),
        ("Accesorio", "Accesorio"),
        ("Otro", "Otro"),
    ]

    solicitud = models.ForeignKey(
        SolicitudProducto,
        on_delete=models.CASCADE,
        related_name="detalles",
    )

    nombre_producto = models.CharField(
        max_length=100
    )

    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIAS,
        default="Videojuego",
    )

    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.nombre_producto} ({self.cantidad})"
