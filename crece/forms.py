from django import forms
from .models import Peticion
from django.contrib.auth.models import User


from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

class PeticionForm(forms.ModelForm):
    class Meta:
        model = Peticion
        fields = ['nombre', 'email', 'telefono', 'mensaje']
