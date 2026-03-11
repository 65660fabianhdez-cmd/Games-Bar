from django.shortcuts import render , redirect
from .models import usuario
# Create your views here.
def pageUsuario (request):
    return render(request,"Usuario.html")

def ingresar_pagina(request):

    if request.method == "POST":

        n_usuario = request.POST['usuario']
        password = request.POST['password']

        try:
            usuario.objects.get(
                nUsuario=n_usuario,
                contrasena=password
                
            )

            return redirect('/pageEntradasSalidas/')

        except usuario.DoesNotExist:

            return render(request, 'Usuario.html', {
                'error': 'Usuario o contraseña incorrectos'
            })
    
    print(usuario)
    print(password)

    return render(request, 'Usuario.html')