from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm, RegistroProfesional
from consultorio.models import Usuario, Paciente, Profesional
from datetime import datetime
from salud_publica_digital.api import API
from json import loads

# Create your views here.
def registro_paciente(request):
    
    if request.method == "POST":
        
        form = RegisterForm(request.POST)
        
        if form.is_valid():

            # Guardar el usuario en la base de datos de DJANGO
            user = form.save()
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(
                username = user.username, 
                password = raw_password
            )

            # Guarda el usuario en la tabla de usuarios
            usuario = Usuario(
                rut = form.cleaned_data.get("username"),
                nombre = form.cleaned_data.get("first_name"),
                apellido = form.cleaned_data.get("last_name"),
                fecha_nacimiento = form.cleaned_data.get("birthdate"),
                direccion = form.cleaned_data.get("address"),
                telefono = form.cleaned_data.get("phone"),
                correo = form.cleaned_data.get("email")
            )
            usuario.save()

            # Guarda el usuario en la tabla de pacientes
            paciente = Paciente(
                usuario = usuario,
                ingreso = datetime.now()
            )
            paciente.save()

            login(request, user)
            
            return redirect("/")
        
        else:
            print(form.errors)
            
    else:
        form = RegisterForm()
        
    return render(
        request = request, 
        template_name = "registro_paciente.html", 
        context = {
            "form": form,
            "title": "Registro de pacientes"
        }
    )

def registro_profesional(request):

    api = API()

    regiones = api.lista_regiones()
    regiones = loads(regiones.content)
    
    if request.method == "POST":
        
        form = RegistroProfesional(request.POST)
        
        if form.is_valid():
            
            # Guardar el usuario en la base de datos de DJANGO
            user = form.save()
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(
                username = user.username, 
                password = raw_password
            )

            # Guarda el usuario en la tabla de usuarios
            usuario = Usuario(
                rut = form.cleaned_data.get("username"),
                nombre = form.cleaned_data.get("first_name"),
                apellido = form.cleaned_data.get("last_name"),
                fecha_nacimiento = form.cleaned_data.get("birthdate"),
                direccion = form.cleaned_data.get("address"),
                telefono = form.cleaned_data.get("phone"),
                correo = form.cleaned_data.get("email")
            )
            usuario.save()

            # Guarda el usuario en la tabla de pacientes
            profesional = Profesional(
                usuario            = usuario,
                especialidad       = form.cleaned_data.get("specialty"),
                rut_profesional    = form.cleaned_data.get("professional_id"),
                titulo_profesional = form.cleaned_data.get("professional_title"),
                c_reg           = form.cleaned_data.get("region"),
                c_com           = form.cleaned_data.get("comuna")
            )
            profesional.save()

            login(request, user)
            
            return redirect("/")
        
        else:
            print(form.errors)
            
    else:
        form = RegistroProfesional()
        
    return render(
        request = request, 
        template_name = "registro_profesional.html", 
        context = {
            "form": form,
            "title": "Registro de profesionales",
            "regiones": regiones
        }
    )