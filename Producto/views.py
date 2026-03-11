from django.shortcuts import render
from .models import Producto_gb

def pageProductos(request):

    productos = Producto_gb.objects.select_related('proveedor').all()

    return render(request, 'Producto.html', {
        'productos': productos
    })