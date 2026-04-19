from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from functools import wraps
from .models import usuario

# Decorador para verificar permisos por rol
def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            username = request.session.get('username')
            role = request.session.get('role')
            if not username or not role:
                return redirect('/pageUsuario/')
            # Si es admin, permitir todo
            if username == 'admin':
                return view_func(request, *args, **kwargs)
            if role not in allowed_roles:
                return HttpResponseForbidden('No tienes permiso para acceder a esta página.')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# Create your views here.
def pageUsuario(request):
    return render(request, 'Usuario.html')


def ingresar_pagina(request):

    if request.method == 'POST':

        n_usuario = request.POST['usuario']
        password = request.POST['password']

        try:
            user = usuario.objects.get(
                nUsuario=n_usuario,
                contrasena=password
            )

            request.session['username'] = user.nUsuario
            request.session['role'] = user.rol

            if user.rol == 'operaciones':
                return redirect('/pageEntradasSalidas/')
            if user.rol == 'proveedor':
                return redirect('/pageProveedores/')
            if user.rol == 'analista_reportes':
                return redirect('/pageReporte/')

        except usuario.DoesNotExist:

            return render(request, 'Usuario.html', {
                'error': 'Usuario o contraseña incorrectos'
            })

    return render(request, 'Usuario.html')


def cerrar_sesion(request):
    request.session.flush()
    return redirect('/pageUsuario/')
