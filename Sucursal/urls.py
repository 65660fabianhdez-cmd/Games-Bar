from django.urls import path
from .views import pageSucursal,crearSucursal, editarSucursal, eliminarSucursal

urlpatterns = [

    path("",pageSucursal),

    path("crearSucursal/",crearSucursal),

    path("editarSucursal/<int:id>/",editarSucursal),

    path("eliminarSucursal/<int:id>/",eliminarSucursal),

]