from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import date

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

class Sugerencia(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='sugerencias', null=True)
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
    descripcion = models.TextField()
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

class Queja(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='quejas', null=True)
    Qfecha = models.DateField(default=date.today)
    RESPONSABLE_CHOICES = [
        ('Comunicacion_cultura', 'Comunicación clima y cultura'),
        ('Desarrollo_laboral', 'Desarrollo y relaciones laborales'),
        ('Nomina_compensaciones', 'Nomina y compensaciones'),
        ('Seguridad_salud_ambiente', 'Seguridad, salud y ambiente'),
        ('Servicios_generales', 'Servicios generales'),
        ('Campo', 'Campo'),
        ('Fabrica', 'Fabrica'),
    ]
    Qresponsable = models.CharField(max_length=50, choices=RESPONSABLE_CHOICES) 
    CAUSA_CHOICES = [
        ('asistencia_tarde', 'Asistencia llegó tarde'),
        ('no_reportado', 'No fue reportado'),
        ('mal_reportado', 'Mal reportado'),
        ('p_sindicales_atrasados', 'P. sindicales atrasados'),
        ('descuentos_atrasados', 'Descuentos atrasados'),
        ('valores_descuento_erroneos', 'Valores de descuento erróneos'),
        ('descuentos_jubilados', 'Descuentos de jubilados'),
    ]
    Qcausa = models.CharField(max_length=30, choices=CAUSA_CHOICES)
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_revision', 'En revisión'),
        ('resuelta', 'Resuelta'),
    ]
    Qestado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    CORREO_CHOICES = [
        ('arongarcia558@gmail.com', 'arongarcia558@gmail.com'),
        ('ggarciap3@unemi.edu.ec', 'ggarciap3@unemi.edu.ec'),
    ]
    correo = models.CharField(max_length=254, choices=CORREO_CHOICES, verbose_name='Correo Electrónico', blank=True, null=True)

class Peticion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='peticion', null=True)
    Pfecha = models.DateField(default=date.today)
    RESPONSABLE_CHOICES = [
        ('Comunicacion_cultura', 'Comunicación clima y cultura'),
        ('Desarrollo_laboral', 'Desarrollo y relaciones laborales'),
        ('Nomina_compensaciones', 'Nomina y compensaciones'),
        ('Seguridad_salud_ambiente', 'Seguridad, salud y ambiente'),
        ('Servicios_generales', 'Servicios generales'),
    ]
    Presponsable = models.CharField(max_length=50, choices=RESPONSABLE_CHOICES) 
    CAUSA_CHOICES = [
        ('actualizacion', 'Actualizar datos'),
        ('no_reportado', 'No fue reportado'),
        ('mal_reportado', 'Mal reportado'),
        ('p_sindicales_atrasados', 'P. sindicales atrasados'),
        ('descuentos_atrasados', 'Descuentos atrasados'),
        ('valores_descuento_erroneos', 'Valores de descuento erróneos'),
        ('descuentos_jubilados', 'Descuentos de jubilados'),
    ]
    Pcausa = models.CharField(max_length=30, choices=CAUSA_CHOICES)
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('resuelta', 'Resuelta'),
    ]
    Pestado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    CORREO_CHOICES = [
        ('arongarcia558@gmail.com', 'arongarcia558@gmail.com'),
        ('ggarciap3@unemi.edu.ec', 'ggarciap3@unemi.edu.ec'),
    ]
    correo = models.CharField(max_length=254, choices=CORREO_CHOICES, verbose_name='Correo Electrónico', blank=True, null=True) 


class Reclamo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reclamo', null=True)
    Rfecha = models.DateField(default=date.today)
    RESPONSABLE_CHOICES = [
        ('Comunicacion_cultura', 'Comunicación clima y cultura'),
        ('Desarrollo_laboral', 'Desarrollo y relaciones laborales'),
        ('Nomina_compensaciones', 'Nomina y compensaciones'),
        ('Seguridad_salud_ambiente', 'Seguridad, salud y ambiente'),
        ('Servicios_generales', 'Servicios generales'),
    ]
    Rresponsable = models.CharField(max_length=50, choices=RESPONSABLE_CHOICES) 
    CAUSA_CHOICES = [
        ('actualizacion', 'Actualizar datos'),
        ('no_reportado', 'No fue reportado'),
        ('mal_reportado', 'Mal reportado'),
        ('p_sindicales_atrasados', 'P. sindicales atrasados'),
        ('descuentos_atrasados', 'Descuentos atrasados'),
        ('valores_descuento_erroneos', 'Valores de descuento erróneos'),
        ('descuentos_jubilados', 'Descuentos de jubilados'),
    ]
    Rcausa = models.CharField(max_length=30, choices=CAUSA_CHOICES)
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_revision', 'En revisión'),
        ('resuelta', 'Resuelta'),
    ]
    Restado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    CORREO_CHOICES = [
        ('arongarcia558@gmail.com', 'arongarcia558@gmail.com'),
        ('ggarciap3@unemi.edu.ec', 'ggarciap3@unemi.edu.ec'),
    ]
    correo = models.CharField(max_length=254, choices=CORREO_CHOICES, verbose_name='Correo Electrónico', blank=True, null=True)