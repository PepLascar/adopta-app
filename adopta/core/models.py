from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# https://www.youtube.com/watch?v=Ae7nc1EGv-A
# https://www.youtube.com/watch?v=sSKYEMEU-C8
# https://docs.djangoproject.com/es/4.0/topics/auth/customizing/

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    #Configuraciones para el panel de administración
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.name

class Article(models.Model):
    articuloid = models.AutoField(primary_key=True, verbose_name="Articulo id")
    title      = models.CharField(max_length=150, verbose_name='Título')
    content    = RichTextField(verbose_name='Contenido')
    image      = models.ImageField(default='null', blank=True, verbose_name='Imagen', upload_to='articles')    #Vincularlo a que carpeta de vicule (la creada en el root llamada media)
    disponible = models.BooleanField(verbose_name='¿Disponible?')
    user       = models.ForeignKey(User, editable=False, verbose_name='Usuario', on_delete=models.CASCADE) # (Editable=False para que el campo no se vea en el editor) Relacionar la ID de los usuarios con el que ha creado el artículo, cascada, se borro el usuario se borra el artículo
    categories = models.ForeignKey(Category, verbose_name='Categoria', on_delete=models.CASCADE, default=True) #blank = True, null=True(para que el campo quede vacío)
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Creado el')    #related name cambia el nombre en la template 
    update_at  = models.DateTimeField(auto_now=True, verbose_name='Editado el')

    class Meta: #Para cuando se muestre en el admin muestre en plural o singular
        verbose_name = 'Artículo'
        verbose_name_plural = 'Artículos'
        ordering = ['-created_at'] # Criterio de orden en página artículos orden descendeente
   
    def __str__(self):  #para cuando llame un objeto obtenga el título
        return self.title
