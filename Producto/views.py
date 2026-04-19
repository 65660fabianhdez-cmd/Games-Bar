from django.shortcuts import render
from .models import Producto_gb
from Usuarios.views import role_required

@role_required(['operaciones'])
def pageProductos(request):

    productos = Producto_gb.objects.select_related('proveedor').all()

    return render(request, 'Producto.html', {
        'productos': productos
    })