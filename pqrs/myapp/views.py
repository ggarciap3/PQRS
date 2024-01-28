import io
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse,Http404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from .models import Usuario,Sugerencia,Queja,Peticion,Reclamo
from .forms import FiltroProcesosForm, SugerenciaForm,QuejaForm,PeticionForm,ReclamoForm
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
#graficos
import plotly.graph_objs as go
from django.db.models import Count
from .models import Sugerencia, Queja, Peticion, Reclamo

from django.db.models.functions import TruncMonth
from django.db.models import Count
from datetime import datetime
from django.contrib.auth.decorators import login_required

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

def formulario_busqueda(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula', '')
        return HttpResponse(f"<a href='/buscar-por-cedula/{cedula}/'>Buscar por cédula</a>")
    else:
        return render(request, 'tu_template.html')

def base_admin(request):
    return render(request, 'base_admin.html')  # Ajusta el nombre del template según tu estructura

def registro(request):
    form = AuthenticationForm()
    # Puedes pasar los formularios correspondientes como contexto
    return render(request, 'registro.html',{'form': form})

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
                causa=request.POST.get('causa'),
                estado=request.POST.get('estado')
            )

            nueva_sugerencia.save()

            sugerencia_data = {
                'cedula': usuario.cedula,
                'nombre_usuario': usuario.nombre,
                'area_usuario': usuario.area,
                'fecha': nueva_sugerencia.fecha,
                'responsable': nueva_sugerencia.responsable,
                'causa': nueva_sugerencia.causa,
                'estado': nueva_sugerencia.estado,
                # Agrega otros campos de Usuario y Sugerencia que desees incluir en la respuesta
            }

            return JsonResponse(sugerencia_data, status=201)

        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado para la creación POST'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def sugerencia_create(request):
    sugerencia = Sugerencia()  # Crear una instancia de Sugerencia
    if request.method == 'POST':
        form = SugerenciaForm(request.POST)
        if form.is_valid():
            usuario = get_object_or_404(Usuario, cedula=request.POST.get('cedula'))
            form.instance.usuario = usuario
            form.save()
            return redirect('registro')  # Redirigir a la página de registro
    else:
        form = SugerenciaForm()

    return render(request, 'sugerencia_create.html', {'form': form, 'sugerencia': sugerencia})

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

@login_required
def lista_admin(request):
    # Configura la cantidad de ítems por página
    items_por_pagina = 4

    # Obtiene los datos para cada tabla
    sugerencias = Sugerencia.objects.all().order_by('-fecha')
    quejas = Queja.objects.all().order_by('-fecha')
    peticiones = Peticion.objects.all().order_by('-fecha')
    reclamos = Reclamo.objects.all().order_by('-fecha')

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

class InformeDownloadView(View):
    def get(self, request, *args, **kwargs):
        # Obtén las fechas de inicio y fin del rango seleccionado (asegúrate de obtenerlas de la solicitud del usuario)
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)

        # Filtra las sugerencias, quejas, peticiones y reclamos por rango de fecha
        sugerencias = Sugerencia.objects.filter(fecha__range=[start_date, end_date]).values()
        quejas = Queja.objects.filter(fecha__range=[start_date, end_date]).values()
        peticiones = Peticion.objects.filter(fecha__range=[start_date, end_date]).values()
        reclamos = Reclamo.objects.filter(fecha__range=[start_date, end_date]).values()

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
    mensaje = f"""Estimado equipo ,

    Se ha registrado una nueva {instance._meta.verbose_name} a nombre del colaborador {instance.usuario.nombre} con CI número {instance.usuario.cedula} con la causa o descripcion {instance.causa}. 
    Para dar atención a la información registrada por el colaborador, ingrese con sus credenciales a la página corporativa.

    Ggarciap3."""
    
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

@login_required        
def update_admin(request):
    sugerencias = Sugerencia.objects.all()
    quejas = Queja.objects.all()
    peticiones = Peticion.objects.all()
    reclamos = Reclamo.objects.all()

    busqueda_usuario = request.GET.get("buscar_usuario")

    if busqueda_usuario:
        sugerencias = sugerencias.filter(usuario__nombre__icontains=busqueda_usuario)
        quejas = quejas.filter(usuario__nombre__icontains=busqueda_usuario)
        peticiones = peticiones.filter(usuario__nombre__icontains=busqueda_usuario)
        reclamos = reclamos.filter(usuario__nombre__icontains=busqueda_usuario)

    return render(request, 'update_admin.html', {
        'sugerencias': sugerencias,
        'quejas': quejas,
        'peticiones': peticiones,
        'reclamos': reclamos
    })

@login_required
def editar_estado(request, modelo, pk):
    # Selecciona el modelo según el nombre proporcionado
    model_map = {
        'Sugerencia': Sugerencia,
        'Queja': Queja,
        'Peticion': Peticion,
        'Reclamo': Reclamo,
    }
    model = model_map.get(modelo)

    # Obtén el objeto específico y prefetch relacionados si es necesario
    objeto = get_object_or_404(model, pk=pk) # type: ignore
    is_sugerencia = isinstance(objeto, Sugerencia)
    # Verifica si el método de solicitud es POST para procesar el formulario de edición
    if request.method == 'POST':
        nuevo_estado = request.POST.get('nuevo_estado')
        doc = request.FILES.get('doc')  # Obtén el archivo adjunto
        objeto.estado = nuevo_estado
        if doc:  # Si se adjuntó un archivo, guardarlo
            objeto.doc = doc
        objeto.save()
        # Redirige a la vista update_admin después de la actualización
        return redirect('update_admin')

    return render(request, 'editar_estado.html', {'objeto': objeto, 'modelo': modelo, 'is_sugerencia': is_sugerencia})

@login_required
def detalle_registro(request, modelo, pk):
    # Obtener el modelo según el nombre proporcionado
    model_map = {
        'Sugerencia': Sugerencia,
        'Queja': Queja,
        'Peticion': Peticion,
        'Reclamo': Reclamo,
    }
    model = model_map.get(modelo)

    # Obtener el registro específico
    registro = get_object_or_404(model, pk=pk) # type: ignore

    # Renderizar la plantilla y pasar el registro al contexto
    return render(request, 'detalle_registro.html', {'registro': registro})

@login_required
def detalle(request, modelo, pk):
    # Obtener el modelo según el nombre proporcionado
    model_map = {
        'Sugerencia': Sugerencia,
        'Queja': Queja,
        'Peticion': Peticion,
        'Reclamo': Reclamo,
    }
    model = model_map.get(modelo)

    # Obtener el registro específico
    registro = get_object_or_404(model, pk=pk) # type: ignore

    # Renderizar la plantilla y pasar el registro al contexto
    return render(request, 'detalle.html', {'registro': registro})

@login_required
def visualizar_procesos(request):
    form = FiltroProcesosForm(request.GET)

    sugerencias = Sugerencia.objects.filter(estado='resuelta')
    quejas = Queja.objects.filter(estado='resuelta')
    peticiones = Peticion.objects.filter(estado='resuelta')
    reclamos = Reclamo.objects.filter(estado='resuelta')

    if form.is_valid():
        cedula = form.cleaned_data.get('cedula')
        responsable = form.cleaned_data.get('responsable')
        tipo_proceso = form.cleaned_data.get('tipo_proceso')

        if cedula:
            sugerencias = sugerencias.filter(usuario__cedula=cedula)
            quejas = quejas.filter(usuario__cedula=cedula)  
            peticiones = peticiones.filter(usuario__cedula=cedula)
            reclamos = reclamos.filter(usuario__cedula=cedula)
        
        if responsable:
            sugerencias = sugerencias.filter(responsable=responsable)
            quejas = quejas.filter(responsable=responsable)
            peticiones = peticiones.filter(responsable=responsable)
            reclamos = reclamos.filter(responsable=responsable)

        if tipo_proceso:
            sugerencias = sugerencias.filter(tipo_proceso=tipo_proceso)
            quejas = quejas.filter(tipo_proceso=tipo_proceso)
            peticiones = peticiones.filter(tipo_proceso=tipo_proceso)
            reclamos = reclamos.filter(tipo_proceso=tipo_proceso)

    return render(request, 'visualizar_procesos.html', {
        'form': form,
        'sugerencias': sugerencias,
        'quejas': quejas,
        'peticiones': peticiones,
        'reclamos': reclamos,
    })

@login_required
def dashboard(request):
    year = datetime.now().year
    month = datetime.now().month

    # Contar registros por mes para cada modelo
    sugerencias_por_mes = Sugerencia.objects.annotate(month=TruncMonth('fecha_registro')).values('month').annotate(count=Count('id')).order_by('month')
    quejas_por_mes = Queja.objects.annotate(month=TruncMonth('fecha_registro')).values('month').annotate(count=Count('id')).order_by('month')
    peticiones_por_mes = Peticion.objects.annotate(month=TruncMonth('fecha_registro')).values('month').annotate(count=Count('id')).order_by('month')
    reclamos_por_mes = Reclamo.objects.annotate(month=TruncMonth('fecha_registro')).values('month').annotate(count=Count('id')).order_by('month')

    # Contar la cantidad de responsables para cada modelo por mes
    counts_sugerencias = Sugerencia.objects.annotate(month=TruncMonth('fecha_registro')).values('month', 'responsable').annotate(count=Count('responsable'))
    counts_quejas = Queja.objects.annotate(month=TruncMonth('fecha_registro')).values('month', 'responsable').annotate(count=Count('responsable'))
    counts_peticiones = Peticion.objects.annotate(month=TruncMonth('fecha_registro')).values('month', 'responsable').annotate(count=Count('responsable'))
    counts_reclamos = Reclamo.objects.annotate(month=TruncMonth('fecha_registro')).values('month', 'responsable').annotate(count=Count('responsable'))

    # Combinar los resultados de cada consulta
    counts_responsables = counts_sugerencias.union(counts_quejas, counts_peticiones, counts_reclamos)

    # Mapear los valores de responsables
    responsable_mapping = {
        'Comunicacion_cultura': 'Comunicación clima y cultura',
        'Desarrollo_laboral': 'Desarrollo y relaciones laborales',
        'Nomina_compensaciones': 'Nomina y compensaciones',
        'Seguridad_salud_ambiente': 'Seguridad, salud y ambiente',
        'Servicios_generales': 'Servicios generales',
        'Campo': 'Campo',
        'Fabrica': 'Fabrica'
    }

    # Obtener los nombres de los responsables y las cantidades por mes
    labels = [responsable_mapping[item['responsable']] for item in counts_responsables]
    values = [item['count'] for item in counts_responsables]

    # Crear el gráfico de pastel
    fig_pie = go.Figure(go.Pie(labels=labels, values=values))
    fig_pie.update_layout(title='Registros por responsables por mes')

    # Convertir el gráfico de pastel a HTML
    plotly_html_pie = fig_pie.to_html(full_html=False)

    # Contar la cantidad de cada tipo de registro por mes
    total_sugerencias = [item['count'] for item in sugerencias_por_mes]
    total_quejas = [item['count'] for item in quejas_por_mes]
    total_peticiones = [item['count'] for item in peticiones_por_mes]
    total_reclamos = [item['count'] for item in reclamos_por_mes]

    # Preparar los datos para el gráfico de barras
    meses = [item['month'] for item in sugerencias_por_mes]  # Se asume que los meses son iguales para todos los tipos de registro
    procesos = ['Sugerencias', 'Quejas', 'Peticiones', 'Reclamos']
    cantidades = [total_sugerencias, total_quejas, total_peticiones, total_reclamos]

    # Crear el gráfico de barras
    fig_bar = go.Figure()

    for i, proceso in enumerate(procesos):
        fig_bar.add_trace(go.Bar(x=meses, y=cantidades[i], name=proceso))

    fig_bar.update_layout(title='Cantidad de Sugerencias, Quejas, Peticiones y Reclamos por Mes', xaxis_title='Mes', yaxis_title='Cantidad')

    # Convertir el gráfico de barras a HTML
    plotly_html_bar = fig_bar.to_html(full_html=False)

    # Pasar los gráficos HTML al contexto
    contexto = {
        'plotly_html_responsables': plotly_html_pie,
        'plotly_html_barras': plotly_html_bar,
        'sugerencias_por_mes': sugerencias_por_mes,
        'quejas_por_mes': quejas_por_mes,
        'peticiones_por_mes': peticiones_por_mes,
        'reclamos_por_mes': reclamos_por_mes
    }

    return render(request, 'dashboard.html', contexto)
