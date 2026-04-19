from datetime import date

from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from Producto.models import Producto_gb
from Proveedor.models import Proveedor_pxn
from Usuarios.views import role_required

from .models import DetalleSolicitudProducto, SolicitudProducto


def _obtener_detalles_formulario(post_data):
    nombres = post_data.getlist("producto[]")
    categorias = post_data.getlist("categoria[]")
    cantidades = post_data.getlist("cantidad[]")

    detalles = []
    errores = []
    total_filas = max(len(nombres), len(categorias), len(cantidades))

    for indice in range(total_filas):
        nombre = (nombres[indice] if indice < len(nombres) else "").strip()
        categoria = (categorias[indice] if indice < len(categorias) else "Videojuego").strip() or "Videojuego"
        cantidad_texto = (cantidades[indice] if indice < len(cantidades) else "").strip()

        if not nombre and not cantidad_texto:
            continue

        if not nombre:
            errores.append(f"Completa el nombre del producto en la fila {indice + 1}.")
            continue

        try:
            cantidad = int(cantidad_texto)
        except (TypeError, ValueError):
            errores.append(f"La cantidad de la fila {indice + 1} debe ser un numero entero.")
            continue

        if cantidad <= 0:
            errores.append(f"La cantidad de la fila {indice + 1} debe ser mayor a 0.")
            continue

        detalles.append(
            {
                "nombre_producto": nombre,
                "categoria": categoria,
                "cantidad": cantidad,
            }
        )

    if not detalles and not errores:
        errores.append("Agrega al menos un producto a la solicitud.")

    return detalles, errores


def _formulario_desde_solicitud(solicitud=None, post_data=None):
    if post_data is not None:
        return {
            "id": post_data.get("solicitud_id", ""),
            "folio": post_data.get("folio", ""),
            "fecha": post_data.get("fecha", ""),
            "proveedor_id": post_data.get("proveedor", ""),
            "observaciones": post_data.get("observaciones", ""),
            "estado": post_data.get("estado", "Pendiente"),
        }

    if solicitud is not None:
        return {
            "id": solicitud.id,
            "folio": solicitud.folio,
            "fecha": solicitud.fecha.isoformat(),
            "proveedor_id": solicitud.proveedor_id,
            "observaciones": solicitud.observaciones,
            "estado": solicitud.estado,
        }

    return {
        "fecha": date.today().isoformat(),
        "estado": "Pendiente",
    }


def _filas_desde_post_data(post_data):
    nombres = post_data.getlist("producto[]")
    categorias = post_data.getlist("categoria[]")
    cantidades = post_data.getlist("cantidad[]")

    filas = []
    total_filas = max(len(nombres), len(categorias), len(cantidades))

    for indice in range(total_filas):
        filas.append(
            {
                "nombre_producto": (nombres[indice] if indice < len(nombres) else "").strip(),
                "categoria": (categorias[indice] if indice < len(categorias) else "Videojuego").strip() or "Videojuego",
                "cantidad": (cantidades[indice] if indice < len(cantidades) else "").strip(),
            }
        )

    return filas or [
        {
            "nombre_producto": "",
            "categoria": "Videojuego",
            "cantidad": "",
        }
    ]


def _filas_desde_solicitud(solicitud=None):
    if solicitud is not None:
        return [
            {
                "nombre_producto": detalle.nombre_producto,
                "categoria": detalle.categoria,
                "cantidad": detalle.cantidad,
            }
            for detalle in solicitud.detalles.all()
        ]

    return [
        {
            "nombre_producto": "",
            "categoria": "Videojuego",
            "cantidad": "",
        }
    ]


def _contexto_solicitudes(formulario=None, filas=None, solicitud_detalle=None, error=None):
    solicitudes = (
        SolicitudProducto.objects.select_related("proveedor")
        .prefetch_related("detalles")
        .all()
    )

    productos_sugeridos = (
        Producto_gb.objects.order_by("nombre_producto")
        .values_list("nombre_producto", flat=True)
        .distinct()
    )

    return {
        "proveedores": Proveedor_pxn.objects.order_by("empresa_prov", "nombre_prov"),
        "solicitudes": solicitudes,
        "productos_sugeridos": productos_sugeridos,
        "categorias": DetalleSolicitudProducto.CATEGORIAS,
        "estados": SolicitudProducto.ESTADOS,
        "solicitud_form": formulario or _formulario_desde_solicitud(),
        "detalle_filas": filas or _filas_desde_solicitud(),
        "solicitud_detalle": solicitud_detalle,
        "modo_edicion": bool(formulario and formulario.get("id")),
        "error": error,
    }


@role_required(['operaciones'])
def Solicitud_Productos(request):
    return render(request, "Solicitud_Productos.html", _contexto_solicitudes())


@role_required(['operaciones'])
def crearSolicitud(request):
    if request.method != "POST":
        return redirect("/pageSolicitudProductos/")

    proveedor_id = request.POST.get("proveedor")
    fecha = request.POST.get("fecha")
    observaciones = request.POST.get("observaciones", "").strip()
    estado = request.POST.get("estado", "Pendiente")

    detalles, errores = _obtener_detalles_formulario(request.POST)

    try:
        proveedor = Proveedor_pxn.objects.get(id=proveedor_id)
    except (Proveedor_pxn.DoesNotExist, ValueError, TypeError):
        proveedor = None
        errores.append("Selecciona un proveedor valido.")

    if not fecha:
        errores.append("Selecciona una fecha para la solicitud.")

    if errores:
        formulario = _formulario_desde_solicitud(post_data=request.POST)
        contexto = _contexto_solicitudes(
            formulario=formulario,
            filas=_filas_desde_post_data(request.POST),
            error=" ".join(errores),
        )
        return render(request, "Solicitud_Productos.html", contexto)

    with transaction.atomic():
        solicitud = SolicitudProducto.objects.create(
            fecha=fecha,
            proveedor=proveedor,
            observaciones=observaciones,
            estado=estado,
        )

        DetalleSolicitudProducto.objects.bulk_create(
            [
                DetalleSolicitudProducto(
                    solicitud=solicitud,
                    nombre_producto=detalle["nombre_producto"],
                    categoria=detalle["categoria"],
                    cantidad=detalle["cantidad"],
                )
                for detalle in detalles
            ]
        )

    return redirect("/pageSolicitudProductos/")


@role_required(['operaciones'])
def verSolicitud(request, id):
    solicitud = get_object_or_404(
        SolicitudProducto.objects.select_related("proveedor").prefetch_related("detalles"),
        id=id,
    )

    return render(
        request,
        "Solicitud_Productos.html",
        _contexto_solicitudes(solicitud_detalle=solicitud),
    )


@role_required(['operaciones'])
def editarSolicitud(request, id):
    solicitud = get_object_or_404(
        SolicitudProducto.objects.select_related("proveedor").prefetch_related("detalles"),
        id=id,
    )

    return render(
        request,
        "Solicitud_Productos.html",
        _contexto_solicitudes(
            formulario=_formulario_desde_solicitud(solicitud=solicitud),
            filas=_filas_desde_solicitud(solicitud=solicitud),
        ),
    )


@role_required(['operaciones'])
def actualizarSolicitud(request, id):
    solicitud = get_object_or_404(
        SolicitudProducto.objects.select_related("proveedor").prefetch_related("detalles"),
        id=id,
    )

    if request.method != "POST":
        return redirect("/pageSolicitudProductos/")

    proveedor_id = request.POST.get("proveedor")
    fecha = request.POST.get("fecha")
    observaciones = request.POST.get("observaciones", "").strip()
    estado = request.POST.get("estado", "Pendiente")

    detalles, errores = _obtener_detalles_formulario(request.POST)

    try:
        proveedor = Proveedor_pxn.objects.get(id=proveedor_id)
    except (Proveedor_pxn.DoesNotExist, ValueError, TypeError):
        proveedor = None
        errores.append("Selecciona un proveedor valido.")

    if not fecha:
        errores.append("Selecciona una fecha para la solicitud.")

    if errores:
        formulario = _formulario_desde_solicitud(post_data=request.POST)
        formulario["id"] = solicitud.id
        formulario["folio"] = solicitud.folio
        contexto = _contexto_solicitudes(
            formulario=formulario,
            filas=_filas_desde_post_data(request.POST),
            error=" ".join(errores),
        )
        return render(request, "Solicitud_Productos.html", contexto)

    with transaction.atomic():
        solicitud.fecha = fecha
        solicitud.proveedor = proveedor
        solicitud.observaciones = observaciones
        solicitud.estado = estado
        solicitud.save()

        solicitud.detalles.all().delete()
        DetalleSolicitudProducto.objects.bulk_create(
            [
                DetalleSolicitudProducto(
                    solicitud=solicitud,
                    nombre_producto=detalle["nombre_producto"],
                    categoria=detalle["categoria"],
                    cantidad=detalle["cantidad"],
                )
                for detalle in detalles
            ]
        )

    return redirect("/pageSolicitudProductos/")


@role_required(['operaciones'])
def eliminarSolicitud(request, id):
    solicitud = get_object_or_404(SolicitudProducto, id=id)

    if request.method == "POST":
        solicitud.delete()

    return redirect("/pageSolicitudProductos/")
