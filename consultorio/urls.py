from django.urls import path
from . import views

urlpatterns = [
    path("reservar_hora", views.reservar_hora, name="reservar_hora"),
    path("agregar_hora", views.agregar_hora, name="agregar_hora"),
    path("error_403", views.error_403, name="error_403"),
    path("configuracion", views.configuracion, name="configuracion"),
    path("seleccionar_hora", views.seleccionar_hora, name="seleccionar_hora"),
    path("reintenta", views.reintenta, name="reintenta"),
]