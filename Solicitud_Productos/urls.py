from django.urls import path

from .views import (
    Solicitud_Productos,
    actualizarSolicitud,
    crearSolicitud,
    editarSolicitud,
    eliminarSolicitud,
    verSolicitud,
)

urlpatterns = [
    path("", Solicitud_Productos),
    path("crearSolicitud/", crearSolicitud),
    path("verSolicitud/<int:id>/", verSolicitud),
    path("editarSolicitud/<int:id>/", editarSolicitud),
    path("actualizarSolicitud/<int:id>/", actualizarSolicitud),
    path("eliminarSolicitud/<int:id>/", eliminarSolicitud),
]
