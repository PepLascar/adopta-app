from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import fields
from .models import Post, Profile, Inbox

class Formulario(UserCreationForm):
    username = forms.CharField(label='Usuario', max_length=30, required=True)
    email = forms.EmailField(max_length=60)
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput, max_length=20)   #que tipo de tag va a ser en el html
    password2 = forms.CharField(label='Confirma contraseña', widget=forms.PasswordInput, max_length=20)

    class Meta:
        model = User
        fields = ['username','email','password1','password2']  #queremos que aparezca
        help_texts = {k:"" for k in fields }  #iterar en campos y poner textos vacíos

#Formulario del post
class PostForm(forms.ModelForm):
	content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':2, 'placeholder': '¿Qué está pasando?'}), required=True, max_length=220) #dandole formato al campo del formulario
                                            #obteniendo campos del contenido
	class Meta:
		model = Post
		fields = ['content']

class InboxForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':2, 'placeholder': '¿Qué está pasando?'}), required=True, max_length=220) #dandole formato al campo del formulario

    class Meta:
        model = Inbox
        fields = ("content",)


# Formulario editar view edit profile
class EditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']