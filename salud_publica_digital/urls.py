"""
URL configuration for salud_publica_digital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from django.contrib import admin
# path: route -> where to forward, view -> what to forward
from django.urls import path, include

# Other views
from registro import views as registro_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .api import API

# All URLs for the project
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/region/", API.as_view(), name="region"),
    path("api/v1/comuna/<int:c_reg>/", API.as_view(), name="lista_comunas"),
    path("api/v1/consultorio/<str:c_com>/", API.as_view(), name="lista_consultorios"),
    path(route="", view=include("principal.urls", "principal"), name="principal"),
    path(route="consultorio/", view=include("consultorio.urls"), name="consultorio"),
    # This will forward all URLs starting with "consultorio/" to the consultorio app
    path(route="registro/", view=registro_views.registro, name="registro"),
    path("", include("django.contrib.auth.urls")),
]