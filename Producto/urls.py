from django.urls import path
from .views import pageProductos 

urlpatterns = [
    path('',pageProductos)
]