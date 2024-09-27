from django.urls import path
from . import views

urlpatterns = [
    path("", views.seleccionar_region, name="consultorio"),
    path("mis_horas", views.mis_horas, name="mis_horas"),
    path("cancelar_hora", views.cancelar_hora, name="cancelar_hora"),
    path("consultorio/obtener_comunas/<int:c_reg>/", views.obtener_comunas, name="obtener_comunas"),
    path("consultorio/obtener_consultorios/<str:c_com>/", views.obtener_consultorios, name="obtener_consultorios"),
]