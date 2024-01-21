import io
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse,Http404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from .models import Usuario,Sugerencia,Queja,Peticion,Reclamo
from .forms import SugerenciaForm,QuejaForm,PeticionForm,ReclamoForm
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Count
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
import pandas as pd

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
import yagmail

# from . import forms

def home(request):
    form = AuthenticationForm()
    return render(request, 'home.html', {'form': form})

class LoginFormView(LoginView):
    template_name = 'home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Iniciar Sesión"
        return context

def cerrar_sesion(request):
    logout(request)
    return redirect('/')

def transferir_datos(request):
    try:
        # Aquí deberías colocar la lógica para transferir datos según tu aplicación
        return HttpResponse("Transferencia de datos exitosa.")
    except Exception as e:
        return HttpResponse(f"Error durante la transferencia de datos: {e}")

def cargar_datos(request):
    try:
        with open('datos_temp.json', 'rb') as file:
            data = file.read().decode('latin-1', errors='replace')

        with open('temp_fixture.json', 'w', encoding='utf-8') as temp_file:
            temp_file.write(data)

        # Lógica adicional para cargar datos en la base de datos si es necesario
        # call_command('loaddata', '--database=default', 'temp_fixture.json')

        return HttpResponse("Transferencia de datos exitosa.")
    except Exception as e:
        return HttpResponse(f"Error durante la transferencia de datos: {e}")

def formulario_busqueda(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula', '')
        return HttpResponse(f"<a href='/buscar-por-cedula/{cedula}/'>Buscar por cédula</a>")
    else:
        return render(request, 'tu_template.html')

def buscar_por_cedula(request, cedula):
    try:
        # Modifica esto según tu modelo y la lógica de búsqueda
        usuario = get_object_or_404(User, username=cedula)
        return HttpResponse(f"Nombre: {usuario.username}, Email: {usuario.email}")
    except Http404:
        return HttpResponse("Usuario no encontrado")

def base_admin(request):
    return render(request, 'base_admin.html')  # Ajusta el nombre del template según tu estructura

def registro(request):
    form = AuthenticationForm()
    # Puedes pasar los formularios correspondientes como contexto
    return render(request, 'registro.html',{'form': form})

def sugerencia_create(request):
    sugerencia = Sugerencia()
    if request.method == 'POST':
        form = SugerenciaForm(request.POST)
        if form.is_valid():
            # Obtén el usuario en función de la cédula o cualquier otro identificador único
            usuario = get_object_or_404(Usuario, cedula=request.POST.get('cedula'))
            form.instance.usuario = usuario
            form.save()
            # Puedes redirigir a una página de éxito o a la lista de sugerencias
            return redirect('registro')
    else:
        form = SugerenciaForm()

    return render(request, 'sugerencia_create.html', {'form': form, 'sugerencia': sugerencia})

def buscar_por_cedula(request, cedula):
    if request.method == 'GET':
        try:
            usuario = get_object_or_404(Usuario, cedula=cedula)

            sugerencia_data = {
                'cedula': usuario.cedula,
                'nombre_usuario': usuario.nombre,
                'area_usuario': usuario.area,
                # Agrega otros campos de Usuario que desees incluir en la respuesta
            }

            return JsonResponse(sugerencia_data, status=200)

        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado para la búsqueda GET'}, status=404)

    elif request.method == 'POST':
        try:
            usuario = get_object_or_404(Usuario, cedula=cedula)  
            nueva_sugerencia = Sugerencia(
                usuario=usuario,
                fecha=request.POST.get('fecha'),
                responsable=request.POST.get('responsable'),
                descripcion=request.POST.get('descripcion'),
                estado=request.POST.get('estado')
            )

            nueva_sugerencia.save()

            sugerencia_data = {
                'cedula': usuario.cedula,
                'nombre_usuario': usuario.nombre,
                'area_usuario': usuario.area,
                'fecha': nueva_sugerencia.fecha,
                'responsable': nueva_sugerencia.responsable,
                'descripcion': nueva_sugerencia.descripcion,
                'estado': nueva_sugerencia.estado,
                # Agrega otros campos de Usuario y Sugerencia que desees incluir en la respuesta
            }

            return JsonResponse(sugerencia_data, status=201)

        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado para la creación POST'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def queja_create(request):
    queja = Queja()
    if request.method == 'POST':
        form = QuejaForm(request.POST)
        if form.is_valid():
            usuario = get_object_or_404(Usuario, cedula=request.POST.get('cedula'))
            form.instance.usuario = usuario
            form.save()
            return redirect('registro')
    else:
        form = QuejaForm()

    return render(request, 'queja_create.html', {'form': form, 'queja': queja})

def peticion_create(request):
    peticion = Peticion()
    if request.method == 'POST':
        form = PeticionForm(request.POST)
        if form.is_valid():
            usuario = get_object_or_404(Usuario, cedula=request.POST.get('cedula'))
            form.instance.usuario = usuario
            form.save()
            return redirect('registro')
    else:
        form = PeticionForm()

    return render(request, 'peticion_create.html', {'form': form, 'peticion': peticion})

def reclamo_create(request):
    reclamo = Reclamo()
    if request.method == 'POST':
        form = ReclamoForm(request.POST)
        if form.is_valid():
            usuario = get_object_or_404(Usuario, cedula=request.POST.get('cedula'))
            form.instance.usuario = usuario
            form.save()
            return redirect('registro')
    else:
        form = ReclamoForm()

    return render(request, 'reclamo_create.html', {'form': form, 'reclamo': reclamo})

def lista_admin(request):
    # Configura la cantidad de ítems por página
    items_por_pagina = 4

    # Obtiene los datos para cada tabla
    sugerencias = Sugerencia.objects.all()
    quejas = Queja.objects.all()
    peticiones = Peticion.objects.all()
    reclamos = Reclamo.objects.all()

    # Pagina los datos
    paginator_sugerencias = Paginator(sugerencias, items_por_pagina)
    paginator_quejas = Paginator(quejas, items_por_pagina)
    paginator_peticiones = Paginator(peticiones, items_por_pagina)
    paginator_reclamos = Paginator(reclamos, items_por_pagina)

    # Obtiene el número de la página solicitada
    page_sugerencias = request.GET.get('page_sugerencias', 1)
    page_quejas = request.GET.get('page_quejas', 1)
    page_peticiones = request.GET.get('page_peticiones', 1)
    page_reclamos = request.GET.get('page_reclamos', 1)

    # Obtiene los objetos de la página solicitada
    try:
        sugerencias = paginator_sugerencias.page(page_sugerencias)
    except PageNotAnInteger:
        sugerencias = paginator_sugerencias.page(1)
    except EmptyPage:
        sugerencias = paginator_sugerencias.page(paginator_sugerencias.num_pages)

    try:
        quejas = paginator_quejas.page(page_quejas)
    except PageNotAnInteger:
        quejas = paginator_quejas.page(1)
    except EmptyPage:
        quejas = paginator_quejas.page(paginator_quejas.num_pages)

    try:
        peticiones = paginator_peticiones.page(page_peticiones)
    except PageNotAnInteger:
        peticiones = paginator_peticiones.page(1)
    except EmptyPage:
        peticiones = paginator_peticiones.page(paginator_peticiones.num_pages)

    try:
        reclamos = paginator_reclamos.page(page_reclamos)
    except PageNotAnInteger:
        reclamos = paginator_reclamos.page(1)
    except EmptyPage:
        reclamos = paginator_reclamos.page(paginator_reclamos.num_pages)

    # Calcula los conteos
    total_reclamo = Reclamo.objects.count()
    total_quejas = Queja.objects.count()
    total_sugerencia = Sugerencia.objects.count()
    total_peticion = Peticion.objects.count()

    return render(request, 'lista_admin.html', {
        'sugerencias': sugerencias,
        'quejas': quejas,
        'peticiones': peticiones,
        'reclamos': reclamos,
        'total_reclamo': total_reclamo,
        'total_quejas': total_quejas,
        'total_sugerencia': total_sugerencia,
        'total_peticion': total_peticion,
    })

class InformeFilterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'informe_template.html')

class InformeDownloadView(View):
    def get(self, request, *args, **kwargs):
        # Obtén las fechas de inicio y fin del rango seleccionado (asegúrate de obtenerlas de la solicitud del usuario)
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)

        # Filtra las sugerencias, quejas, peticiones y reclamos por rango de fecha
        sugerencias = Sugerencia.objects.filter(fecha__range=[start_date, end_date]).values()
        quejas = Queja.objects.filter(Qfecha__range=[start_date, end_date]).values()
        peticiones = Peticion.objects.filter(Pfecha__range=[start_date, end_date]).values()
        reclamos = Reclamo.objects.filter(Rfecha__range=[start_date, end_date]).values()

        # Crea DataFrames de pandas con los datos
        df_sugerencias = pd.DataFrame(sugerencias)
        df_quejas = pd.DataFrame(quejas)
        df_peticiones = pd.DataFrame(peticiones)
        df_reclamos = pd.DataFrame(reclamos)

        # Crea un escritor Excel en memoria con pandas
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='openpyxl')

        # Guarda los DataFrames en hojas de Excel
        df_sugerencias.to_excel(writer, sheet_name='Sugerencias', index=False)
        df_quejas.to_excel(writer, sheet_name='Quejas', index=False)
        df_peticiones.to_excel(writer, sheet_name='Peticiones', index=False)
        df_reclamos.to_excel(writer, sheet_name='Reclamos', index=False)

        # Cierra el escritor
        writer.close()

        # Obtén el contenido
        output.seek(0)

        # Crea la respuesta de Django con el archivo Excel en memoria
        response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=informe.xlsx'

        return response

@receiver(post_save, sender=Sugerencia)
@receiver(post_save, sender=Queja)
@receiver(post_save, sender=Peticion)
@receiver(post_save, sender=Reclamo)
def enviar_correo_despues_de_guardar(sender, instance, **kwargs):
    mensaje = f"""Estimado equipo de Servicio al cliente,

    Se ha registrado una nueva {instance._meta.verbose_name} a nombre del colaborador {instance.usuario.nombre} con CI número {instance.usuario.cedula} con la causa o descripcion {instance.causa}. 
    Para dar atención a la información registrada por el colaborador, ingrese con sus credenciales a la página corporativa.

    Wall-eat."""
    
    # Aquí deberías obtener el correo del modelo correspondiente, por ejemplo:
    correo_electronico = instance.correo

    # Luego, llama a la función enviar_correo_registro con el correo_electronico correcto
    enviar_correo_registro(correo_electronico, mensaje, instance._meta.verbose_name_plural)

# Método para enviar correo
def enviar_correo_registro(correo, mensaje, verbose_name_plural):
    try:
        # Conecta con el servidor SMTP de yagmail
        yag = yagmail.SMTP("wall.eat.co@gmail.com", "rcundbofzdotxfbv")

        # Envia el correo electrónico
        yag.send(to=correo, subject=f"Ingreso de {verbose_name_plural}", contents=mensaje)
    except Exception as e:
        # Maneja cualquier excepción que pueda ocurrir durante el envío del correo
        print(f"Error al enviar correo: {e}")
