from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from salud_publica_digital.api import API
from .reserva import Reserva
from utils.db import insert, upsert
from json import loads
from secrets import token_hex
from consultorio.models import Paciente, Profesional

# Create your views here.

def error_403(request: HttpRequest):
    return render(
        request = request, 
        template_name = "error_403.html", 
        context = {"title": "Error 403"}
    )

def reintenta(request: HttpRequest):
    return render(
        request = request, 
        template_name = "reintenta.html", 
        context = {"title": "Error 500"}
    )

def configuracion(request: HttpRequest):

    api = API()
    
    regiones = api.lista_regiones()
    regiones = loads(regiones.content)

    if request.method == "POST":
        
        data = {
            "c_reg": request.POST["region"],
            "c_com": request.POST["comuna"],
            "rut"  : request.user.username # type: ignore
        }

        upsert(
            db_name = "salud_publica_digital",
            name    = "atencion",
            field   = "rut",
            data    = data
        )

        return redirect("/")

    return render(
        request = request, 
        template_name = "configuracion.html", 
        context = {
            "title": "Configuración",
            "regiones": regiones
        }
    )

@login_required(login_url='/login/')
def confirmar_hora(request: HttpRequest, context: dict):

    profesional = Profesional.objects.filter(usuario_id=request.user.username) # type: ignore

    if profesional.exists():
        return error_403(request)

    insert(
        db_name = "salud_publica_digital",
        name    = "reserva",
        data    = context
    )

    return redirect("/")

@login_required(login_url='/login/')
def seleccionar_hora(request: HttpRequest):

    profesional = Profesional.objects.filter(usuario_id=request.user.username) # type: ignore

    if profesional.exists():
        return error_403(request)
    
    consultorio_id = request.session["reserva"]["consultorio_id"]

    api = API()
    horas = api.lista_horas(consultorio_id=consultorio_id)

    horas = loads(horas.content)

    if not horas:
        return reintenta(request)
    
    horas = horas[0]
    hora_inicial, hora_final = horas["horas"].split(",")

    rango_horas = range(
        int(hora_inicial), 
        int(hora_final) + 1
    )
    
    if request.method == "POST":
        
        request.session["reserva"]["hora"] = request.POST["hora"]

        return confirmar_hora(request, request.session["reserva"])

    return render(
        request = request, 
        template_name = "seleccionar_hora.html", 
        context = {
            "title": "Seleccionar hora",
            "horas": rango_horas
        }
    )

@login_required(login_url='/login/')
def reservar_hora(request: HttpRequest):

    profesional = Profesional.objects.filter(usuario_id=request.user.username) # type: ignore

    if profesional.exists():
        return error_403(request)
    
    api = API()
    
    regiones = api.lista_regiones()
    regiones = loads(regiones.content)
    
    form = Reserva(data=request.POST)

    if form.is_valid():
    
        if request.method == "POST":
            
            consultorio_id = form.data["consultorio"]

            consultorio    = loads(
                api.get_consultorio(consultorio_id=consultorio_id).content
            )[0]
            
            latitud, longitud = consultorio["latitud"], consultorio["longitud"]
            
            data = {
                "id"         :    token_hex(nbytes=16),
                "rut"        :    request.user.username, # type: ignore
                "region"     :    form.data["region"],
                "comuna"     :    form.data["comuna"],
                "consultorio_id": consultorio_id,
                "consultorio":    consultorio["nombre"],
                "latitud":        latitud,
                "longitud":       longitud,
                "motivo"     :    form.data["motivo"],
                "fecha"      :    form.data["fecha"]
            }

            request.session["reserva"] = data
            
            # Insert reservation into the database
            return redirect("seleccionar_hora")
        
        # Handle form processing
        return redirect("/")   
    
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
def agregar_hora(request: HttpRequest):

    paciente = Paciente.objects.filter(usuario_id=request.user.username) # type: ignore

    if paciente.exists():
        return error_403(request)
    
    api = API()

    localizacion = api.get_atencion_profesional(rut=request.user.username) # type: ignore

    try:
        c_com = loads(localizacion.content)[0]["c_com"]
    except IndexError:
        return configuracion(request)
    
    consultorios = api.lista_consultorios(c_com=c_com)
    consultorios = loads(consultorios.content)

    if request.method == "POST":
        
        data = {
            "consultorio_id": request.POST["consultorio"],
            "horas": request.POST["horas"],
            "rut"  : request.user.username # type: ignore
        }

        upsert(
            db_name = "salud_publica_digital",
            name    = "horas",
            field   = "rut",
            data    = data
        )

        return redirect("/")

    return render(
        request = request, 
        template_name = "agregar_hora.html", 
        context = {
            "title": "Agregar hora",
            "consultorios": consultorios
        }
    )