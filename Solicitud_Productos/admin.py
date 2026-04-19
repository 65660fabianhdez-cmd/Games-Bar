from django.contrib import admin

from .models import DetalleSolicitudProducto, SolicitudProducto


class DetalleSolicitudInline(admin.TabularInline):
    model = DetalleSolicitudProducto
    extra = 0


@admin.register(SolicitudProducto)
class SolicitudProductoAdmin(admin.ModelAdmin):
    list_display = ("folio", "fecha", "proveedor", "estado")
    search_fields = ("folio", "proveedor__empresa_prov", "proveedor__nombre_prov")
    list_filter = ("estado", "fecha")
    inlines = [DetalleSolicitudInline]
