from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Peticion,Post, Comment
from .forms import PeticionForm, PostForm, CommentForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse


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

############ vista para foro

def foro(request):
    posts = Post.objects.all()
    return render(request, 'crece/html/foro/foro.html', {'posts': posts})

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return JsonResponse({'success': True, 'post_id': post.pk, 'title': post.title, 'content': post.content})
    return JsonResponse({'success': False})

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user and not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'No tienes permiso para editar esta publicación'})

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return JsonResponse({'success': True, 'post_id': post.pk, 'title': post.title, 'content': post.content})
    return JsonResponse({'success': False})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'crece/html/foro/post_detail.html', {'post': post, 'form': form})

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'No tienes permiso para eliminar esta publicación'})

    if request.method == 'POST':
        post.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})