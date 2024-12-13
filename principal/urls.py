from django.urls import path
from . import views

app_name = "principal"

urlpatterns = [
    path("", views.home, name="principal"),
    path("seleccion_usuario", views.seleccion_usuario, name="seleccion_usuario")
]