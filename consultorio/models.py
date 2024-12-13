from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    rut = models.CharField(max_length=12, primary_key=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField()
    direccion = models.EmailField(null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    correo = models.EmailField(max_length=255)
    
    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f'{self.rut}'
    
class Profesional(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='profesional')
    especialidad = models.CharField(max_length=255)
    rut_profesional = models.CharField(max_length=12, unique=True, null=True)
    titulo_profesional = models.CharField(max_length=255, null=True, blank=True)
    c_reg = models.CharField(max_length=255, null=True, blank=True)
    c_com = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'profesional'
        verbose_name_plural = 'profesionales'
        ordering = ["usuario", "especialidad"]

    def __str__(self):
        return f'{self.usuario.rut}'
    
class Paciente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='paciente')
    ingreso = models.DateField()

    class Meta:
        verbose_name = 'paciente'
        verbose_name_plural = 'pacientes'
        ordering = ["usuario", "ingreso"]

    def __str__(self):
        return f'{self.usuario.rut}'