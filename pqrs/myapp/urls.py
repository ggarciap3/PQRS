from django.urls import path
from .views import home, LoginFormView, transferir_datos, buscar_por_cedula, cargar_datos, base_admin, cerrar_sesion, sugerencia_create, registro, queja_create, peticion_create, reclamo_create


urlpatterns = [
    path('', home, name='index'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('cerrar-sesion/', cerrar_sesion, name='cerrar_sesion'),
    path('base-admin/', base_admin, name='base_admin'),  # Mantuve el guion bajo para consistencia
    path('transferir-datos/', transferir_datos, name='transferir_datos'),
    path('cargar-datos/', cargar_datos, name='cargar_datos'),
    path('registro/', registro, name='registro'),
    path('buscar-por-cedula/<str:cedula>/', buscar_por_cedula, name='buscar_por_cedula'),
    path('sugerencias/create/', sugerencia_create, name='sugerencia_create'),

    path('quejas/create/', queja_create, name='queja_create'),

    path('peticiones/create/', peticion_create, name='peticion_create'),
    path('reclamos/create/', reclamo_create, name='reclamo_create'),

]
