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
        
        auth_header = request.META['HTTP_AUTHORIZATION']
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]
        
        user = authenticate(username=username, password=password)
        
        if user:
            
            url = request.get_full_path()
            
            if "comuna" in url:
                
                return self.obtener_comunas(request, kwargs['c_reg'])
            
            elif "consultorio" in url:
                
                return self.obtener_consultorios(request, kwargs['c_com'])
            
            elif "region" in url:
                
                return self.lista_regiones(request)
        
        else:
            
            return JsonResponse({'error': 'Credenciales incorrectas.'}, status=400)
    
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

    def obtener_comunas(self, request, c_reg):
        comunas = (
            Consultorio
            .objects
            .filter(c_reg=c_reg)
            .values('c_com', 'nom_com')
            .distinct()
            .order_by('nom_com')
        )
        return JsonResponse(list(comunas), safe=False)

    def obtener_consultorios(self, request, c_com):
        consultorios = (
            Consultorio
            .objects
            .filter(c_com=c_com)
            .values()
        )
        return JsonResponse(list(consultorios), safe=False)