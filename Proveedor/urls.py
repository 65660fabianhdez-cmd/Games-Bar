from django.urls import path
from .views import Proveedor, sumar_proveedor, eliminar_proveedor,editar_proveedor, actualizar_proveedor

urlpatterns = [
    path('',Proveedor),
    path('sumar_proveedor/',sumar_proveedor),
    path('eliminar_proveedor/<int:id>/', eliminar_proveedor),
    path('editar_proveedor/<int:id>/', editar_proveedor),
    path('actualizar_proveedor/<int:id>/', actualizar_proveedor),]