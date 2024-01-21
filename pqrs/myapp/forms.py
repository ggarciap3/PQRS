from django import forms
from .models import Sugerencia, Queja, Peticion, Reclamo

class SugerenciaForm(forms.ModelForm):
    class Meta:
        model = Sugerencia
        fields = ['fecha', 'responsable', 'descripcion', 'estado', 'correo']

    def clean_usuario(self):
        # Devuelve el valor del campo usuario aunque esté deshabilitado
        return self.cleaned_data.get('usuario')

class QuejaForm(forms.ModelForm):
    class Meta:
        model = Queja
        fields = ['Qfecha', 'Qresponsable', 'Qcausa', 'Qestado', 'correo']

    def clean_usuario(self):
        # Devuelve el valor del campo usuario aunque esté deshabilitado
        return self.cleaned_data.get('usuario')
    
class PeticionForm(forms.ModelForm):
    class Meta:
        model = Peticion
        fields = ['Pfecha', 'Presponsable', 'Pcausa', 'Pestado', 'correo']

    def clean_usuario(self):
        # Devuelve el valor del campo usuario aunque esté deshabilitado
        return self.cleaned_data.get('usuario')

class ReclamoForm(forms.ModelForm):
    class Meta:
        model = Reclamo
        fields = ['Rfecha', 'Rresponsable', 'Rcausa', 'Restado', 'correo']

    def clean_usuario(self):
        # Devuelve el valor del campo usuario aunque esté deshabilitado
        return self.cleaned_data.get('usuario')