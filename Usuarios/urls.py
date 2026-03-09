from django.urls import path
from .views import Usuario, login

urlpatterns = [
    path("", Usuario),
    path("/login", login)
]