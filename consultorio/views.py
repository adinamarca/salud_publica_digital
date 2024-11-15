from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from salud_publica_digital.api import API
from .reserva import Reserva
from .db import insert_reserva, list_reservas
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
    
    reservas = list_reservas(request.user.username)
    
    return render(
        request = request, 
        template_name = "mis_horas.html", 
        context = {
            "title": "Mis horas",
            "reservas": reservas
        }
    )

@login_required(login_url='/login/')
def reservar_hora(request: HttpRequest):
    
    api = API()
    
    regiones = api.lista_regiones()
    regiones = loads(regiones.content)
    
    form = Reserva(data=request.POST)
    
    if request.method == "POST":
        
        if form.is_valid():
            
            data = {
                "rut"        : request.user.username,
                "region"     : form.data["region"],
                "comuna"     : form.data["comuna"],
                "consultorio": form.data["consultorio"],
                "motivo"     : form.data["motivo"],
                "fecha"      : form.data["fecha"]
            }
            
            # Insert reservation into the database
            insert_reserva(data)
            
            # Handle form processing
            return redirect("mis_horas")
            
    
    return render(
        request       = request, 
        template_name = "reservar_hora.html", 
        context       = {
            "title"   : "Reservar hora",
            "regiones": regiones,
            "form"    : form
        }
    )

@login_required(login_url='/login/')
def cancelar_hora(request: HttpRequest):
    return render(
        request = request, 
        template_name = "cancelar_hora.html", 
        context = {"title": "Cancelar hora"}
    )