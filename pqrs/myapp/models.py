from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import date
from django.utils import timezone

class Usuario(models.Model):
    cedula = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=255)
    area = models.CharField(max_length=50)
    departamento = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50)
    tipo_empleado = models.CharField(max_length=20)
    tipo_contrato = models.CharField(max_length=20)

    class Meta:
        db_table = 'usuario'

class Registro(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='%(class)ss', null=True)
    fecha = models.DateField(default=date.today)
    RESPONSABLE_CHOICES = [
        ('Comunicacion_cultura', 'Comunicación clima y cultura'),
        ('Desarrollo_laboral', 'Desarrollo y relaciones laborales'),
        ('Nomina_compensaciones', 'Nomina y compensaciones'),
        ('Seguridad_salud_ambiente', 'Seguridad, salud y ambiente'),
        ('Servicios_generales', 'Servicios generales'),
        ('Campo', 'Campo'),
        ('Fabrica', 'Fabrica'),
    ]
    responsable = models.CharField(max_length=50, choices=RESPONSABLE_CHOICES)
    causa = models.TextField()
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_revision', 'En revisión'),
        ('resuelta', 'Resuelta'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    CORREO_CHOICES = [
        ('arongarcia558@gmail.com', 'arongarcia558@gmail.com'),
        ('ggarciap3@unemi.edu.ec', 'ggarciap3@unemi.edu.ec'),
    ]
    correo = models.CharField(max_length=254, choices=CORREO_CHOICES, verbose_name='Correo Electrónico', blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True
    
class Sugerencia(Registro):
    tipo_proceso = models.CharField(max_length=20, default='Sugerencia')
    

class Queja(Registro):
    CAUSA_CHOICES = [
        ('asistencia_tarde', 'Asistencia llegó tarde'),
        ('no_reportado', 'No fue reportado'),
        ('mal_reportado', 'Mal reportado'),
        ('p_sindicales_atrasados', 'P. sindicales atrasados'),
        ('descuentos_atrasados', 'Descuentos atrasados'),
        ('valores_descuento_erroneos', 'Valores de descuento erróneos'),
        ('descuentos_jubilados', 'Descuentos de jubilados'),
    ]
    causa = models.CharField(max_length=30, choices=CAUSA_CHOICES)
    doc = models.FileField(upload_to='documentos/', blank=True, null=True)
    tipo_proceso = models.CharField(max_length=20, default='Queja')

class Peticion(Registro):
    CAUSA_CHOICES = [
        ('actualizacion', 'Actualizar datos'),
        ('no_reportado', 'No fue reportado'),
        ('mal_reportado', 'Mal reportado'),
        ('p_sindicales_atrasados', 'P. sindicales atrasados'),
        ('descuentos_atrasados', 'Descuentos atrasados'),
        ('valores_descuento_erroneos', 'Valores de descuento erróneos'),
        ('descuentos_jubilados', 'Descuentos de jubilados'),
    ]
    causa = models.CharField(max_length=30, choices=CAUSA_CHOICES)
    doc = models.FileField(upload_to='documentos/', blank=True, null=True)
    tipo_proceso = models.CharField(max_length=20, default='Peticion')

class Reclamo(Registro):
    CAUSA_CHOICES = [
        ('actualizacion', 'Actualizar datos'),
        ('no_reportado', 'No fue reportado'),
        ('mal_reportado', 'Mal reportado'),
        ('p_sindicales_atrasados', 'P. sindicales atrasados'),
        ('descuentos_atrasados', 'Descuentos atrasados'),
        ('valores_descuento_erroneos', 'Valores de descuento erróneos'),
        ('descuentos_jubilados', 'Descuentos de jubilados'),
    ]
    causa = models.CharField(max_length=30, choices=CAUSA_CHOICES)
    doc = models.FileField(upload_to='documentos/', blank=True, null=True)
    tipo_proceso = models.CharField(max_length=20, default='Reclamo')