from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm #Lo dejé de usar para personalizar register form.
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required #Decoradores
from .forms import RegisterForm, FormArticle #RegisterForm de forms.py
from .models import Category, Article
from social.models import Post

# https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html

def home(req):
    return render(req, 'home.html')


def listar(req):
    articles = Article.objects.all() # Traer/obtener todos los objetos (articulos)
    return render(req, 'listar.html', {
        'title': 'Artículos',
        'articles': articles
    })

@login_required(login_url='login')
def crear(req): 
    if req.method == 'POST':
        formulario = FormArticle(req.POST, files=req.FILES)  
        if formulario.is_valid(): # is_valid evalua las condiciones de validacion que se configuran
            data_form = formulario.cleaned_data # Datos limpios que llegan del formulario           
            user = getattr(req, 'user', None)
            title = data_form.get('title')
            categories = data_form.get('categories')
            content = data_form.get('content') # Variables para recoger la información del cleaned data
            disponible = 1
            image = data_form.get('image')
                            
            articulo = Article(
                user = user,
                title = title,
                categories = categories,
                content = content,
                disponible = 1,
                image = image
            )
            articulo.save()           
            print(f'Articulo creado: {articulo}')           
            messages.success(req, ' ' ) # Flash message que se muestra 1 vez(al actualizar)
            return redirect('listar')
            #return HttpResponse(articulo.title + ' - ' + articulo.content+' - ' + str(articulo.public))
    else:
        formulario = FormArticle()
        print('Else Line 46')
    return render(req, 'crear.html', {
        'form': formulario       
    })

@login_required(login_url='login')
def editPet(req, pk):
    articulo = get_object_or_404(Article, articuloid=pk) # Variable con objeto Article proveniente del modelo
    data = {
        'title': 'Edita los datos de tu mascota',
        'form': FormArticle(instance=articulo)
    }   
    CurrentUserId = req.user.id
    idPetOwner = articulo.user_id

    if CurrentUserId != idPetOwner:
        print('El usuario no tiene permisos para editar') # Redirect si la mascota no pertenece al usuario
        return redirect('listar')
    elif req.method == 'POST': # Validar form solo para peticiones POST
        formulario_edit = FormArticle(data=req.POST, instance=articulo, files=req.FILES)  # Conjunto de datos a grabar, mediante la instancia del objeto
        if formulario_edit.is_valid:
            formulario_edit.save()
            messages.success(req, 'Datos de mascota editados')
            print(f'Line 69 Mascota editada > {articulo}')
            return redirect('profile')
    return render(req, 'editPet.html', data)

@login_required(login_url='login')
def eliminar(req, pk):
    articulo = get_object_or_404(Article, articuloid=pk) # Instancia del articulo a eliminar, id obtenida desde views
    idPetOwner = articulo.user_id
    userId = req.user.id #logged user
    if userId == idPetOwner:
        articulo.delete() # Eliminar el objeto instanciado
        messages.success(req, 'Mascota eliminada')
        print(f'Line 81: Mascota eliminada > {articulo}')
    else:
        print('Line 82: El usuario no tiene permisos para editar')
    #Agregar alerta cuando redirija al profile  
    return redirect('profile')

def category(req, category_id):
    category = Category.objects.get(id=category_id)
    return render(req, 'categories/category.html', {
        'category': category
        #'articles': articles
    })

# @login_required
# def profile(request, username=None):  #obteniendo perfil de los usuarios, vía url que visitan
# 	current_user = request.user #usuario logueda
# 	if username and username != current_user.username:
# 		user = User.objects.get(username=username)#revisar si quiero visitar un usuario cualquiera
# 		posts = user.posts.all()
# 		userId = request.user.id
# 		pet = Article.objects.all().filter(user_id=user)
# 	else:
# 		posts = current_user.posts.all()#mostrar todos los post que el usuario ha hecho
# 		user = current_user
# 		userId = request.user.id
# 		pet = Article.objects.all().filter(user_id=userId)
# 		print(pet)		
# 	return render(request, 'social/profile.html', {'user':user, 'posts':posts, 'pet':pet})

@login_required
def stats(req):
    username = req.user.username #usuario logueda
    # print(f'{username} (Antes del if else)')
    # user = User.objects.get(pk=username)

    disponibles = Article.objects.all().filter(disponible=1).count()
    noDisp = Article.objects.all().filter(disponible=0).count()
    totalAnimales = Article.objects.all().count()
    perros = Article.objects.all().filter(categories_id=1).count()
    gatos = Article.objects.all().filter(categories_id=2).count()
    otros = Article.objects.all().filter(categories_id=3).count()
    totalUsuarios = User.objects.all().count()
    totalFeed = Post.objects.all().count()

    promedioMascotasUsuario = round(totalAnimales/totalUsuarios, 1)
    porcentajePetAdoptadas = round((disponibles/totalAnimales)*100, 1)
    promedioMensajesUsuario = round((totalFeed/totalUsuarios), 1)

    data = {
        'disp': disponibles,
        'noDisp': noDisp,
        'totalAnimales': totalAnimales,
        'perros': perros,
        'gatos': gatos,
        'otros': otros,
        'totalUsuarios': totalUsuarios,
        'totalFeed': totalFeed,
        'porcentajePetAdoptadas':porcentajePetAdoptadas,
        'promedioMensajesUsuario':promedioMensajesUsuario,
        'promedioMascotasUsuario':promedioMascotasUsuario
    }
    # print(f'Mascotas disponibles {disponibles}')
    # print(f'Mascotas no disponibles {noDisp}')
    # tot = Article.objects.annotate(Count('disponible'))
    # print(tot)
    print(username)
    if username == 'admin':
        print(f'Current user: {username} (IF)')
        return render(req, 'stats.html', data)
    else:
        print(f'Current user: {username} (ELSE)')
        return redirect('listar')

def error404_view(request, exception):
    return render(request, '404.html')