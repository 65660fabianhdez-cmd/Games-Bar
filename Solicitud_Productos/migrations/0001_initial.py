# Generated manually to enable Solicitud_Productos persistence.

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("Proveedor", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SolicitudProducto",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("folio", models.CharField(blank=True, max_length=25, null=True, unique=True)),
                ("fecha", models.DateField(default=django.utils.timezone.now)),
                ("observaciones", models.TextField(blank=True)),
                ("estado", models.CharField(choices=[("Pendiente", "Pendiente"), ("En proceso", "En proceso"), ("Completada", "Completada"), ("Cancelada", "Cancelada")], default="Pendiente", max_length=20)),
                ("proveedor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="solicitudes_producto", to="Proveedor.proveedor_pxn")),
            ],
            options={
                "ordering": ["-fecha", "-id"],
            },
        ),
        migrations.CreateModel(
            name="DetalleSolicitudProducto",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre_producto", models.CharField(max_length=100)),
                ("categoria", models.CharField(choices=[("Videojuego", "Videojuego"), ("Consola", "Consola"), ("Control", "Control"), ("Accesorio", "Accesorio"), ("Otro", "Otro")], default="Videojuego", max_length=20)),
                ("cantidad", models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ("solicitud", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="detalles", to="Solicitud_Productos.solicitudproducto")),
            ],
            options={
                "ordering": ["id"],
            },
        ),
    ]
