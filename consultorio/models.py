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
    
class Paciente(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    class Meta:
        verbose_name = 'paciente'
        verbose_name_plural = 'pacientes'
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

class Reserva(models.Model):
    consultorio = models.ForeignKey(Consultorio, on_delete=models.CASCADE, related_name='reservas')
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='reservas')
    fecha_reserva = models.DateTimeField()
    motivo = models.TextField()

    class Meta:
        verbose_name = 'reserva'
        verbose_name_plural = 'reservas'
        ordering = ['fecha_reserva']

    def __str__(self):
        return f'Reserva de {self.paciente} en {self.consultorio.nombre} el {self.fecha_reserva}'