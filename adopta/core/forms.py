from django.forms import ModelForm, fields
from django import forms #formularios
from django.core import validators #validadores
from django.contrib.auth.forms import UserCreationForm # formularios por defecto
from django.contrib.auth.models import User  # modelo de Usuario para crear el formulario
from .models import Article

class RegisterForm(UserCreationForm): # formulario creado en base a una clase llamada RegisterForm, hereda de UserCreationForm
    class Meta:
        model  = User  #modelo en el cual se va a basar el formulario
        fields = [
            'username',
            'email',
            'first_name', #campos que tiene el modelo para representar visualmente en el formulario
            'last_name',
            'password1',
            'password2']

class FormArticle(forms.ModelForm): #Heredar de form para obtener los campos(fields)
    class Meta:
        model = Article
        fields = [
            'articuloid',
            'title',
            'categories',
            'content',
            'disponible',
            'image']