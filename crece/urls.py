from django.urls import path
from . import views


urlpatterns = [

    #Vistas normales
    path('', views.index, name='index2'),
    path('index/', views.index, name='index'),
    path('actividades/', views.actividades, name='actividades'),
    path('grupos/', views.grupos, name='grupos'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('puente/', views.puente, name='puente'),

    path('peticiones/', views.lista_peticiones, name='lista_peticiones'),
    path('peticiones/nueva/', views.crear_peticion, name='crear_peticion'),
    path('peticiones/<int:pk>/editar/', views.actualizar_peticion, name='actualizar_peticion'),
    path('peticiones/<int:pk>/eliminar/', views.eliminar_peticion, name='eliminar_peticion'),

    path('register/', views.registro, name='register'),

    # Foro paths
    path('foro/foro', views.foro, name='foro'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),

]
