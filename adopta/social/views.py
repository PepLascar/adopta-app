from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from core.models import Category, Article
from django.contrib import messages
from .forms import EditForm, Formulario, PostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import DeferredAttribute

def feed(request):
	posts = Post.objects.all()
	context = {'posts': posts}
	return render(request, 'social/feed.html', context)

def register(request):
	if request.method == 'POST':
		form = Formulario(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			form.save()
			messages.success(request, f'¡Bienvenido a la comunidad {username}, ahora puedes ingresar!')
			return redirect('login')
	else:
		form = Formulario()
	context = {'form': form}
	return render(request, 'social/register.html', context)

@login_required
def post(request):
	current_user = get_object_or_404(User, pk=request.user.pk)
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = current_user
			post.save()
			messages.success(request, 'Posteando ... ')
			return redirect('feed')
	else:
		form = PostForm()
	return render(request, 'social/post.html', {'form' : form })
#--------------------------------------------------------------------------------------------------------------------------#
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
#--------------------------------------------------------------------------------------------------------------------------#
@login_required
def follow(request, username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user
	rel = Relationship(from_user=current_user, to_user=to_user_id) #crear relation ship
	rel.save()
	messages.success(request, f'Ahora sigues a {username}')
	return redirect('feed')

@login_required
def unfollow(request, username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user.id
	rel = Relationship.objects.filter(from_user=current_user.id, to_user=to_user_id).get()  #buscar la relationship del model
	rel.delete()
	messages.success(request, f'Ya no sigues a {username}')
	return redirect('feed')

@login_required
def editProfile(request, pk):
	perfil = Profile.objects.get(user_id=pk) #traer objeto del model
	datos = {
		'form': EditForm(instance=perfil)
	}
	if request.method == 'POST':
		formulario_edit = EditForm(data=request.POST, instance=perfil, files=request.FILES)  #conjunto de datos a grabar, mediante la instancia del objeto
		data=request.POST
		files=request.FILES
		if formulario_edit.is_bound == False:		
			formulario_edit.save()
			messages.success(request, 'Foto de perfil editada') #REVISAR QUE ESTABA HACIENDO ACA
			print('FALSE')
			print(data)			
			return redirect('profile')
		if formulario_edit.is_bound == True:		
			formulario_edit.save()
			messages.success(request, 'Foto de perfil editada')
			print('TRUE')
			print(data)
			return redirect('profile')
	print('con 99')
	return render(request, 'social/editar.html', datos)

def eliminarpost(req):
	return None