from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Peticion
from .forms import PeticionForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

# Create your views here.

def index(request):
    context = {}
    return render(request, 'crece/index.html', context)

def actividades(request):
    context = {}
    return render(request, 'crece/html/actividades.html', context)

def grupos(request):
    context = {}
    return render(request, 'crece/html/grupos.html', context)

def nosotros(request):
    context = {}
    return render(request, 'crece/html/nosotros.html', context)

def peticiones(request):
    context = {}
    return render(request, 'crece/html/peticiones.html', context)

def puente(request):
    context = {}
    return render(request, 'crece/html/puente.html', context)

def foro(request):
    context = {}
    return render(request, 'crece/html/foro/foro.html', context)

###############################################################
######################## C R U D ##############################
###############################################################


def lista_peticiones(request):
    peticiones = Peticion.objects.all()
    return render(request, 'crece/html/lista_peticiones.html', {'peticiones': peticiones})


def crear_peticion(request):
    if request.method == 'POST':
        form = PeticionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_peticiones')
    else:
        form = PeticionForm()
    return render(request, 'crece/html/crear_peticion.html', {'form': form})

@login_required
def actualizar_peticion(request, pk):
    peticion = get_object_or_404(Peticion, pk=pk)
    if request.method == 'POST':
        form = PeticionForm(request.POST, instance=peticion)
        if form.is_valid():
            form.save()
            return redirect('lista_peticiones')
    else:
        form = PeticionForm(instance=peticion)
    return render(request, 'crece/html/crear_peticion.html', {'form': form})

@login_required
def eliminar_peticion(request, pk):
    peticion = get_object_or_404(Peticion, pk=pk)
    if request.method == 'POST':
        peticion.delete()
        return redirect('lista_peticiones')
    return render(request, 'crece/html/eliminar_peticion.html', {'peticion': peticion})


@login_required
def registro(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        mensaje = None  # Inicializa el mensaje como None

        if password1 != password2:
            mensaje = "Las contraseñas no coinciden."
        elif User.objects.filter(username=username).exists():
            mensaje = "El nombre de usuario ya está en uso."
        elif User.objects.filter(email=email).exists():
            mensaje = "El correo ya se encuentra registrado."
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            user = authenticate(username=username, password=password1)
            if user is not None:
                login(request, user)
                mensaje = f"¡Cuenta creada para {username}!"
                return redirect("index")  # Redirige a la página de inicio o donde prefieras

        context = {'mensaje': mensaje}
        return render(request, "registration/register.html", context)
    
    return render(request, "registration/register.html")

