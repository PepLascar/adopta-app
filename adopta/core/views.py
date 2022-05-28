from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm #Lo dejé de usar para personalizar register form.
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, FormArticle #RegisterForm de forms.py
from django.contrib.auth.decorators import login_required #Decoradores
from .models import Category, Article
from django.contrib.auth.models import User

# https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html

@login_required(login_url="login") #Decorador, lista, articulos, etc
def index(req):
    print('en index')
    return render (req, 'index.html', {
        'title': 'Inicio'
    })

# --- Listar Artículos con Categorías ---
@login_required(login_url='login')
def crear(request): 
    if request.method == 'POST':
        print("Método post")
        formulario = FormArticle(request.POST, files=request.FILES)  
        if formulario.is_valid(): # is_valid evalúa las condiciones de validación que se configuran
            print("Consola 139")
            data_form = formulario.cleaned_data # Datos limpios que llegan del formulario           
            user = getattr(request, 'user', None)
            title   = data_form.get('title')
            content = data_form.get('content') # Variables para recoger la información del cleaned data
            disponible  = data_form['disponible']
            image = data_form.get('image')
                            
            articulo = Article(
                user = user,
                title = title,
                content = content,
                disponible = disponible,
                image = image
            )
            print(f'Usuario loguedo: {user}')
            articulo.save()
            
            # Crear mensaje flash que solo de muestra 1 vez(actualización)
            messages.success(request, ' ' )
            return redirect('listar')
            #return HttpResponse(articulo.title + ' - ' + articulo.content+' - ' + str(articulo.public))
    else:
        formulario = FormArticle()
        print("Consola 145")
    return render(request, 'crear.html', {
        'form': formulario       
    })

def listar(req):
    articles = Article.objects.all() # Traer/obtener todos los objetos (articulos)
    return render(req, 'listar.html', {
        'title': 'Artículos',
        'articles': articles
    })

def editar(req, pk):
    articulo = Article.objects.get(articuloid=pk) # Variable con objeto Article del modelo
    print(f'oo Editando ... oo {articulo}')
    datos = {
        'title': 'Edita los datos de tu mascota',
        'form': FormArticle(instance=articulo)
    }
    # print('141 141')
    if req.method == 'POST':
        formulario_edit = FormArticle(data=req.POST, instance=articulo, files=req.FILES)  # Conjunto de datos a grabar, mediante la instancia del objeto
        if formulario_edit.is_valid:
            formulario_edit.save()
            datos['mensaje'] = "Vehículo Editado Correctamente"
            messages.success(req, f'Has editado correctamente el artículo {articulo.articuloid}: {articulo.title}' )
            return redirect('listar')  
    return render(req, 'editar.html', datos)

@login_required(login_url='login')
def eliminar(req, pk):
    current_user = request.user
    if username and username != current_user.username:
        articulo = Article.objects.get(pk=pk) # Instancia del articulo que quiero eliminar, id obtenida desde views
        articulo.delete() # Elimino ese objeto instanciado 
        print(f'Eliminado {articulo}')
    else:
        user = current_user
        userId= request.user.id
    return redirect('profile')

def category(req, category_id):
    category = Category.objects.get(id=category_id)
    return render(req, 'categories/category.html', {
        'category': category
        #'articles': articles
    })
# ---- 
# ---- 
@login_required
def profile(request, username=None):  #obteniendo perfil de los usuarios, a trave´s de la url se visitan
	current_user = request.user #usuario logueda
	if username and username != current_user.username: 
		user = User.objects.get(username=username)#revisar si quiero visitar un usuario cuañquiera
		posts = user.posts.all()
		userId= request.user.id	
		pet= Article.objects.all().filter(user_id=user)
		# print(username)
		# print(current_user.username)
		# print(username) #USUARIO CON EL QUE ESTOY LOGUADO
		# print(current_user.username)
	else:
		posts = current_user.posts.all()#mostrar todos los post que el usuario ha hecho
		user = current_user
		userId= request.user.id
		pet = Article.objects.all().filter(user_id=userId)
		print(pet)		
	return render(request, 'social/profile.html', {'user':user, 'posts':posts, 'pet':pet})
    