from django.shortcuts import render, redirect, get_object_or_404
from .models import Sucursal
from Usuarios.views import role_required

@role_required(['operaciones'])
def pageSucursal(request):

    sucursales = Sucursal.objects.all()

    return render(request, "sucursal.html", {
        "sucursales": sucursales
    })

@role_required(['operaciones'])
def crearSucursal(request):

    if request.method == "POST":

        nombre = request.POST.get("nombre")
        direccion = request.POST.get("direccion")
        ciudad = request.POST.get("ciudad")
        telefono = request.POST.get("telefono")
        encargado = request.POST.get("encargado")
        email = request.POST.get("email")
        horario = request.POST.get("horario")
        estado = request.POST.get("estado")

        Sucursal.objects.create(
            nombre=nombre,
            direccion=direccion,
            ciudad=ciudad,
            telefono=telefono,
            encargado=encargado,
            email=email,
            horario=horario,
            estado=estado
        )

    return redirect("/pageSucursal/")


@role_required(['operaciones'])
def editarSucursal(request, id):

    sucursal = get_object_or_404(Sucursal, id=id)

    if request.method == "POST":

        sucursal.nombre = request.POST.get("nombre")
        sucursal.direccion = request.POST.get("direccion")
        sucursal.ciudad = request.POST.get("ciudad")
        sucursal.telefono = request.POST.get("telefono")
        sucursal.encargado = request.POST.get("encargado")
        sucursal.email = request.POST.get("email")
        sucursal.horario = request.POST.get("horario")
        sucursal.estado = request.POST.get("estado")

        sucursal.save()

        return redirect("/pageSucursal/")

    return render(request,"editarSucursal.html", {
        "sucursal": sucursal
    })

@role_required(['operaciones'])
def eliminarSucursal(request, id):

    sucursal = get_object_or_404(Sucursal, id=id)

    sucursal.delete()

    return redirect("/pageSucursal/")
