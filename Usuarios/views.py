from django.shortcuts import render , redirect
from .models import usuario
# Create your views here.
def Usuario (request):
    return render(request,"Usuario.html")

def login(request):

    if request.method == "POST":

        usuario = request.POST['usuario']
        contrasena = request.POST['contrasena']

        try:
            user = Usuario.objects.get(
                nUsuario=usuario,
                contrasena=contrasena
            )

            return redirect('/inicio/')

        except Usuario.DoesNotExist:
            return render(request,'login.html',{
                'error': 'Usuario o contraseña incorrectos'
            })

    return render(request,'login.html')