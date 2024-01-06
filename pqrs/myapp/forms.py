from django import forms
from .models import Sugerencia , Queja

class SugerenciaForm(forms.ModelForm):
    class Meta:
        model = Sugerencia
        fields = ['fecha', 'responsable', 'descripcion', 'estado']

    def clean_usuario(self):
        # Devuelve el valor del campo usuario aunque esté deshabilitado
        return self.cleaned_data.get('usuario')

class QuejaForm(forms.ModelForm):
    class Meta:
        model = Queja
        fields = ['Qfecha', 'Qresponsable', 'Qcausa', 'Qestado']

    def clean_usuario(self):
        # Devuelve el valor del campo usuario aunque esté deshabilitado
        return self.cleaned_data.get('usuario')