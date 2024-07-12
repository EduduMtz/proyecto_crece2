from django import forms
from .models import Peticion, Post, Comment
from django.contrib.auth.models import User


from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

class PeticionForm(forms.ModelForm):
    class Meta:
        model = Peticion
        fields = ['nombre', 'email', 'telefono', 'mensaje']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
