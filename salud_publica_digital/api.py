from django.http import JsonResponse
from consultorio.models import Consultorio
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth import authenticate
from base64 import b64decode

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
        
        regiones = (
            Consultorio
            .objects
            .values('c_reg', 'nom_reg')
            .distinct()
            .order_by('c_reg')
        )
        
        # Parse float to int
        for region in regiones:
            region['c_reg'] = int(region['c_reg'])
        
        return JsonResponse(list(regiones), safe=False)

    def lista_comunas(self, request = None, c_reg = None):
        
        comunas = (
            Consultorio
            .objects
            .filter(c_reg=c_reg)
            .values('c_com', 'nom_com')
            .distinct()
            .order_by('nom_com')
        )
        return JsonResponse(list(comunas), safe=False)

    def lista_consultorios(self, request = None, c_com = None):
        
        consultorios = (
            Consultorio
            .objects
            .filter(c_com=c_com)
            .values()
        )
        return JsonResponse(list(consultorios), safe=False)