from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from .models import Consultorio

def seleccionar_region(request):
    regiones = Consultorio.objects.values('c_reg', 'nom_reg').distinct().order_by('c_reg')
    return render(request, 'consultorio.html', {'regiones': regiones})

def obtener_comunas(request, c_reg):
    comunas = (
        Consultorio
        .objects
        .filter(c_reg=c_reg)
        .values('c_com', 'nom_com')
        .distinct()
        .order_by('nom_com')
    )
    return JsonResponse(list(comunas), safe=False)

def obtener_consultorios(request, c_com):
    consultorios = (
        Consultorio
        .objects
        .filter(c_com=c_com)
        .values()
    )
    return JsonResponse(list(consultorios), safe=False)

# Create your views here.
def home(request: HttpRequest):
    return render(
        request = request, 
        template_name = "consultorio.html", 
        context = {"title": "Página principal del consultorio"}
    )

def mis_horas(request: HttpRequest):
    return render(
        request = request, 
        template_name = "mis_horas.html", 
        context = {"title": "Mis horas"}
    )

def reservar_hora(request: HttpRequest):
    return render(
        request = request, 
        template_name = "reservar_hora.html", 
        context = {"title": "Reservar hora"}
    )

def cancelar_hora(request: HttpRequest):
    return render(
        request = request, 
        template_name = "cancelar_hora.html", 
        context = {"title": "Cancelar hora"}
    )