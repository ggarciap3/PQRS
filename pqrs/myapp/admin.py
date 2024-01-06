from django.contrib import admin
from .models import Usuario, Sugerencia, Queja

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['cedula', 'nombre', 'area', 'departamento', 'cargo', 'tipo_empleado', 'tipo_contrato']

class SugerenciaAdmin(admin.ModelAdmin):
    list_display = ['id','cedula','nombre', 'area', 'fecha','descripcion', 'responsable','estado' ]
    
    def cedula(self, obj):
        return obj.usuario.cedula if obj.usuario else ""
   
    def nombre(self, obj):
        return obj.usuario.nombre if obj.usuario else ""

    def area(self, obj):
        return obj.usuario.area if obj.usuario else ""

    # Añade campos relacionados al modelo Sugerencia en la interfaz de administración
    search_fields = ['usuario__cedula','usuario__nombre', 'usuario__area', 'descripcion']

class QuejaAdmin(admin.ModelAdmin):
    list_display = ['id','cedula','nombre', 'area', 'Qfecha', 'Qresponsable', 'Qcausa', 'Qestado' ]

    def cedula(self, obj):
        return obj.usuario.cedula if obj.usuario else ""

    def nombre(self, obj):
        return obj.usuario.nombre if obj.usuario else ""

    def area(self, obj):
        return obj.usuario.area if obj.usuario else ""

    # Añade campos relacionados al modelo Queja en la interfaz de administración
    search_fields = ['usuario__cedula','usuario__nombre', 'usuario__area', 'descripcion']


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Sugerencia, SugerenciaAdmin)
admin.site.register(Queja, QuejaAdmin)