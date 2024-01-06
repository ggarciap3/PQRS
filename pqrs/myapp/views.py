from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse,Http404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from .models import Usuario,Sugerencia,Queja,Peticion,Reclamo
from .forms import SugerenciaForm,QuejaForm,PeticionForm,ReclamoForm
from django.contrib.auth.models import User
from django.conf import settings
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
        form = QuejaForm(request.POST)
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
        form = QuejaForm(request.POST)
        if form.is_valid():
            usuario = get_object_or_404(Usuario, cedula=request.POST.get('cedula'))
            form.instance.usuario = usuario
            form.save()
            return redirect('registro')
    else:
        form = ReclamoForm()

    return render(request, 'reclamo_create.html', {'form': form, 'reclamo': reclamo})