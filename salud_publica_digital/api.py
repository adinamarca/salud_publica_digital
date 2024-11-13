from django.shortcuts import render
from django.http import JsonResponse
from consultorio.models import Consultorio
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

class API(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @classmethod
    def post(cls, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': token.key}, status=200)
        else:
            return JsonResponse({'error': 'Credenciales inválidas'}, status=400)
    
    @classmethod
    def lista_regiones(cls):
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

    @classmethod
    def obtener_comunas(cls, request, c_reg):
        comunas = (
            Consultorio
            .objects
            .filter(c_reg=c_reg)
            .values('c_com', 'nom_com')
            .distinct()
            .order_by('nom_com')
        )
        return JsonResponse(list(comunas), safe=False)

    @classmethod
    def obtener_consultorios(cls, request, c_com):
        consultorios = (
            Consultorio
            .objects
            .filter(c_com=c_com)
            .values()
        )
        return JsonResponse(list(consultorios), safe=False)