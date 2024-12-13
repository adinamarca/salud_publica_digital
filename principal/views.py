from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from consultorio.models import Paciente, Profesional
from utils.db import list_items

# Create your views here.
def home(request: HttpRequest):

    reservas = list_items(
        db_name = "salud_publica_digital",
        name    = "reserva",
        field   = "rut",
        value   = request.user.username # type: ignore
    )

    profesional = Profesional.objects.filter(usuario_id=request.user.username)

    if not profesional.exists():

        return render(
            request = request, 
            template_name = "principal_paciente.html", 
            context = {
                "title": "Página principal paciente",
                "reservas": reservas
            }
        )
    
    return render(
        request = request, 
        template_name = "principal_profesional.html", 
        context = {
            "title": "Página principal profesional",
            "reservas": reservas,
            "profesional": profesional.first()
        }
    )

def seleccion_usuario(request: HttpRequest):

    return render(
        request = request, 
        template_name = "seleccion_usuario.html", 
        context = {
            "title": "Tipo de usuario",
        }
    )