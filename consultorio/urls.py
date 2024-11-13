from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("reservar_hora", views.reservar_hora, name="reservar_hora"),
    path("mis_horas", views.mis_horas, name="mis_horas"),
    path("cancelar_hora", views.cancelar_hora, name="cancelar_hora")
]