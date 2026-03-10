from django.shortcuts import render,redirect
from .models import Proveedor_pxn
# Create your views here.
def Proveedor(request):
    proveedores = Proveedor_pxn.objects.all()
    return render(request, "Proveedor.html", {"proveedores": proveedores})

def sumar_proveedor(request):

    if request.method == "POST":
        proveedor = Proveedor_pxn(
            empresa_prov=request.POST['empresa_prov'],
            nombre_prov=request.POST['nombre_prov'],
            contacto_prov=request.POST['contacto_prov']
        )
        proveedor.save()

    return redirect('/pageProveedores/')

def eliminar_proveedor(request, id):
    provedor = Proveedor_pxn.objects.get(id=id)
    provedor.delete()
    return redirect('/pageProveedores/')

def editar_proveedor(request, id):

    proveedor = Proveedor_pxn.objects.get(id=id)

    return render(request, "Proveedor.html", {
        "proveedor": proveedor
    })


def actualizar_proveedor(request, id):

    proveedor = Proveedor_pxn.objects.get(id=id)

    if request.method == "POST":
        proveedor.empresa_prov = request.POST['empresa_prov']
        proveedor.nombre_prov = request.POST['nombre_prov']
        proveedor.contacto_prov = request.POST['contacto_prov']

        proveedor.save()

    return redirect('/pageProveedores/')
