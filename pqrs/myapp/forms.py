from django import forms
from .models import Sugerencia, Queja, Peticion, Reclamo


class SugerenciaForm(forms.ModelForm):
    class Meta:
        model = Sugerencia
        fields = ['fecha', 'responsable', 'causa', 'estado', 'correo']

    def clean_usuario(self):
        # Devuelve el valor del campo usuario aunque esté deshabilitado
        return self.cleaned_data.get('usuario')

class QuejaForm(forms.ModelForm):
    class Meta:
        model = Queja
        fields = ['fecha', 'responsable', 'causa', 'estado', 'correo']

    def clean_usuario(self):
        # Devuelve el valor del campo usuario aunque esté deshabilitado
        return self.cleaned_data.get('usuario')
    
class PeticionForm(forms.ModelForm):
    class Meta:
        model = Peticion
        fields = ['fecha', 'responsable', 'causa', 'estado', 'correo']

    def clean_usuario(self):
        # Devuelve el valor del campo usuario aunque esté deshabilitado
        return self.cleaned_data.get('usuario')

class ReclamoForm(forms.ModelForm):
    class Meta:
        model = Reclamo
        fields = ['fecha', 'responsable', 'causa', 'estado', 'correo']

    def clean_usuario(self):
        # Devuelve el valor del campo usuario aunque esté deshabilitado
        return self.cleaned_data.get('usuario')

class FiltroProcesosForm(forms.Form):
    RESPONSABLE_CHOICES = [
        ('', 'Seleccione...'),
        ('Comunicacion_cultura', 'Comunicación clima y cultura'),
        ('Desarrollo_laboral', 'Desarrollo y relaciones laborales'),
        ('Nomina_compensaciones', 'Nomina y compensaciones'),
        ('Seguridad_salud_ambiente', 'Seguridad, salud y ambiente'),
        ('Servicios_generales', 'Servicios generales'),
        ('Campo', 'Campo'),
        ('Fabrica', 'Fabrica'),
    ]

    TIPO_CHOICES = [
        ('', 'Seleccione...'),
        ('Sugerencia', 'Sugerencia'),
        ('Queja', 'Queja'),
        ('Peticion', 'Petición'),
        ('Reclamo', 'Reclamo'),
    ]

    tipo_proceso = forms.ChoiceField(choices=TIPO_CHOICES, required=False)
    responsable = forms.ChoiceField(choices=RESPONSABLE_CHOICES, required=False)
    cedula = forms.CharField(max_length=10, required=False)
    
    