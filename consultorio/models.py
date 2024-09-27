from django.db import models

# Create your models here.
class Consultorio(models.Model):
    objectid  = models.IntegerField(primary_key=True)
    nombre    = models.CharField(max_length=255)
    c_reg     = models.FloatField()
    nom_reg   = models.CharField(max_length=255)
    c_com     = models.CharField(max_length=10)
    nom_com   = models.CharField(max_length=255)
    c_ant     = models.CharField(max_length=10)
    c_vig     = models.FloatField()
    c_mad     = models.CharField(max_length=10)
    c_nmad    = models.CharField(max_length=10)
    c_depend  = models.FloatField()
    depen     = models.CharField(max_length=255)
    perenec   = models.CharField(max_length=255)
    tipo      = models.CharField(max_length=255)
    ambito    = models.CharField(max_length=255)
    urgencia  = models.CharField(max_length=3)
    certifica = models.CharField(max_length=3)
    depen_a   = models.CharField(max_length=255)
    nivel     = models.CharField(max_length=255)
    via       = models.CharField(max_length=255)
    numero    = models.CharField(max_length=10)
    direccion = models.CharField(max_length=255)
    fono      = models.CharField(
        max_length=255, 
        null=True, 
        blank=True
    )
    f_inicio  = models.FloatField()
    f_reaper  = models.CharField(max_length=255)
    sapu      = models.CharField(max_length=255)
    f_cambio  = models.CharField(max_length=255)
    tipo_camb = models.CharField(max_length=255)
    prestador = models.CharField(max_length=255)
    estado    = models.CharField(max_length=255)
    nivel_com = models.CharField(max_length=255)
    modalidad = models.CharField(max_length=255)
    latitud   = models.FloatField()
    longitud  = models.FloatField()

    class Meta:
        verbose_name = 'consultorio'
        verbose_name_plural = 'consultorios'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre