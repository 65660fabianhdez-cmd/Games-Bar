from django.urls import path
from .views import (
    pageUsuario,
    ingresar_pagina,
    cerrar_sesion,
)

urlpatterns = [
    path('', pageUsuario),
    path('login/', ingresar_pagina),
    path('logout/', cerrar_sesion),
]