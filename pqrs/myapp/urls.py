from django.urls import path
from . import views
from .views import home, LoginFormView, buscar_por_cedula, base_admin, cerrar_sesion, sugerencia_create, registro, queja_create, peticion_create, reclamo_create, lista_admin
from .views import InformeDownloadView,update_admin,visualizar_procesos,dashboard
urlpatterns = [
    path('', home, name='index'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('cerrar-sesion/', cerrar_sesion, name='cerrar_sesion'),
    path('base-admin/', base_admin, name='base_admin'),  # Mantuve el guion bajo para consistencia
    path('registro/', registro, name='registro'),
    path('buscar-por-cedula/<str:cedula>/', buscar_por_cedula, name='buscar_por_cedula'),
    path('sugerencias/create/', sugerencia_create, name='sugerencia_create'),
    path('quejas/create/', queja_create, name='queja_create'),
    path('peticiones/create/', peticion_create, name='peticion_create'),
    path('reclamos/create/', reclamo_create, name='reclamo_create'),
    path('lista-admin/', lista_admin, name='lista_admin'),
    path('informe/download/', InformeDownloadView.as_view(), name='informe_download'),
    path('update_admin/', update_admin, name='update_admin'),
    path('editar_estado/<str:modelo>/<int:pk>/', views.editar_estado, name='editar_estado'),
    path('detalle_registro/<str:modelo>/<int:pk>/', views.detalle_registro, name='detalle_registro'),
    path('detalle/<str:modelo>/<int:pk>/', views.detalle, name='detalle'),
    path('procesos_terminados/', visualizar_procesos, name='procesos_terminados'),
    path('dashboard/', dashboard, name='dashboard'),
]   
