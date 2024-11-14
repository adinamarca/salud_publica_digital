from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from salud_publica_digital.api import API
from json import loads

# Create your views here.
def home(request: HttpRequest):
    return render(
        request = request, 
        template_name = "consultorio.html", 
        context = {"title": "Página principal del consultorio"}
    )

@login_required(login_url='/login/')
def mis_horas(request: HttpRequest):
    return render(
        request = request, 
        template_name = "mis_horas.html", 
        context = {"title": "Mis horas"}
    )

@login_required(login_url='/login/')
def reservar_hora(request: HttpRequest):
    
    api = API()
    
    regiones = api.lista_regiones()
    regiones = loads(regiones.content)
    
    return render(
        request = request, 
        template_name = "reservar_hora.html", 
        context = {
            "title": "Reservar hora",
            "regiones": regiones
        }
    )

@login_required(login_url='/login/')
def cancelar_hora(request: HttpRequest):
    return render(
        request = request, 
        template_name = "cancelar_hora.html", 
        context = {"title": "Cancelar hora"}
    )