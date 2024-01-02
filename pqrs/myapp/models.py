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
        ('FARIAS', 'FARIAS'),
        ('GGARCIA', 'GGARCIA'),
        ('WMARUDENA', 'WMARUDENA'),
        ('NANDALUZ', 'NANDALUZ'),
    ]
    responsable = models.CharField(max_length=20, choices=RESPONSABLE_CHOICES)
    descripcion = models.TextField()
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('revisado', 'Revisado'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)

    # def autocompletar_campos(self):
    #     # Llenar los campos nombre y area basándote en el usuario asociado
    #     if self.usuario:
    #         self.nombre = self.usuario.nombre
    #         self.area = self.usuario.area

# @receiver(pre_save, sender=Sugerencia)
# def pre_save_sugerencia(sender, instance, **kwargs):
#     instance.autocompletar_campos()
