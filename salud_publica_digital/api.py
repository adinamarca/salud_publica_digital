from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth import authenticate
from base64 import b64decode
from utils.db import list_items

class API(APIView):
    
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        
        authenticated = False
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if auth_header is not None:
            
            encoded_credentials = auth_header.split(" ")[1]  # Removes "Basic " to isolate credentials
            decoded_credentials = (
                b64decode(encoded_credentials)
                .decode("utf-8")
                .split(":")
            )
            username = decoded_credentials[0]
            password = decoded_credentials[1]
            user = authenticate(username=username, password=password)
            authenticated = (True if user else False)
            
        else:
            authenticated = request.user.is_authenticated
            
        if authenticated:
            url = request.get_full_path()
            
            if "comuna" in url:
                response = self.lista_comunas(request, kwargs['c_reg'])
            
            elif "consultorio" in url:
                response = self.lista_consultorios(request, kwargs['c_com'])
            
            elif "region" in url:
                response = self.lista_regiones(request)
        
        else:
            response = JsonResponse({'error': 'Credenciales incorrectas.'}, status=400)
            
        return response
    
    def lista_regiones(self, request = None):

        regiones = list_items(
            db_name  = "salud_publica_digital",
            name     = "consultorio"
        )
        
        regiones = sorted(regiones, key=lambda x: x['c_reg'])
        # Remove duplicates
        regiones = dict((x['c_reg'], x) for x in regiones).values()
        
        # Parse float to int
        for region in regiones:
            region['c_reg'] = int(region['c_reg'])
        
        return JsonResponse(list(regiones), safe=False)

    def lista_comunas(self, request = None, c_reg = None):

        comunas = list_items(
            db_name = "salud_publica_digital",
            name    = "consultorio",
            field   = "c_reg",
            value   = c_reg
        )
        
        comunas = sorted(comunas, key=lambda x: x['c_com'])
        # Remove duplicates
        comunas = dict((x['c_com'], x) for x in comunas).values()

        return JsonResponse(list(comunas), safe=False)

    def lista_consultorios(self, request = None, c_com = None):
        
        consultorios = list_items(
            db_name = "salud_publica_digital",
            name    = "consultorio",
            field   = "c_com",
            value   = c_com
        )

        return JsonResponse(list(consultorios), safe=False)
    
    def get_consultorio(self, request = None, consultorio_id = None):

        if consultorio_id is not None:
            consultorio_id = int(consultorio_id)
        
        consultorio = list_items(
            db_name = "salud_publica_digital",
            name    = "consultorio",
            field   = "objectid",
            value   = consultorio_id
        )

        return JsonResponse(list(consultorio), safe=False)
    
    def get_atencion_profesional(self, request = None, rut = None):

        atencion = list_items(
            db_name = "salud_publica_digital",
            name    = "atencion",
            field   = "rut",
            value   = rut
        )

        return JsonResponse(list(atencion), safe=False)
    
    def lista_horas(self, request = None, consultorio_id = None):

        horas = list_items(
            db_name = "salud_publica_digital",
            name    = "horas",
            field   = "consultorio_id",
            value   = str(consultorio_id)
        )

        return JsonResponse(list(horas), safe=False)