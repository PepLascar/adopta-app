from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from core.models import Category, Article
from django.contrib import messages
from .forms import EditForm, Formulario, PostForm, InboxForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import DeferredAttribute
from django.contrib.auth.views import LoginView

@login_required
def feed(request):
	current_user = get_object_or_404(User, pk=request.user.pk)
	posts = Post.objects.all()
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = current_user
			post.save()
			messages.success(request, 'Posteando ... ')
			return redirect('feed')
	else:
		posting = True
		form = PostForm()

	context = {	'posts': posts, 
				'form' : form,
				'posting': posting }
	return render(request, 'social/feed.html', context)

def mail(request, id):
	pet = Article.objects.filter(articuloid=id)
	if request.method == 'POST':
		messages.success(request, 'Enviando correo ... ')
		return redirect('feed')
	return render(request, 'social/mail.html', {'pet':pet})

@login_required
def petProfile(req, id):
	pet = get_object_or_404(Article, articuloid=id)
	petList = Article.objects.all()
	getOwner = pet.user_id
	owner = User.objects.get(id=getOwner)
	data ={ 'pet':pet,
			'petList':petList,
			'owner':owner}
	return render(req, 'social/petProfile.html', data)

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
def inbox(request, id):
	current_user = get_object_or_404(User, pk=request.user.pk) #Usuario logueado
	to_user_id = User.objects.get(id=id) #Usuario del perfil que me encuentro
	inboxs = Inbox.objects.all()
	toId = int(id)

	#Crear funcion desde el controlador para ya mandar los datos filtrados (cómo en def profile)
	inbox_current_user = Inbox.objects.all().filter(to_user_id=to_user_id)
	inbox_sender = Inbox.objects.all().filter(sender_id=current_user)
	data ={ 'inboxs':inboxs,
			'current':current_user,
			'current_inbox':inbox_current_user,
			'inbox_sender':inbox_sender,
			'to':to_user_id,
			'toId':toId, }

	if request.method == 'POST':
		form = InboxForm(request.POST)
		if form.is_valid():
			data_form = form.cleaned_data
			sender = current_user
			to_user = to_user_id
			content = data_form.get('content')

			inbox = Inbox(
				sender = sender,
				to_user = to_user,
				content = content
			)
			inbox.save()
			print(f'Inbox creado') 
			messages.success(request, f'Enviando inbox a {to_user_id.username}')
			return redirect('inbox', id=to_user_id.id)
			# return render(request, 'social/chat.html')
	else:
		form = PostForm()
		print('else inbox 78')
	return render(request, 'social/inbox.html', data)

@login_required
def chats(request):
	current_user = get_object_or_404(User, pk=request.user.id) # Usuario logueado
	inboxs = Inbox.objects.all()
	users = User.objects.all()

	#tengo que mandar el sender id sin repetir
	to_user = set(Inbox.objects.all().filter(to_user_id=current_user).values_list('sender_id', flat=True).distinct())
	sender_user = set(Inbox.objects.all().filter(sender_id=current_user).values_list('to_user_id', flat=True).distinct())
	
	senders = to_user | sender_user

	print(f'Senders: {senders}')
	print(f'{sender_user}')
	print(f'{to_user}')
	return render(request, 'social/chat.html', {'to_user':to_user, 'sender_user':sender_user, 'current_user':current_user, 'inboxs':inboxs, 'users':users, 'senders':senders})

@login_required
def profile(request, username=None):  # obteniendo perfil de los usuarios, a trave´s de la url se visitan
	current_user = request.user # usuario logueda
	if username and username != current_user.username: 
		user = get_object_or_404(User, username=username)# revisar si quiero visitar un usuario cuañquiera
		posts = user.posts.all()
		userId= request.user.id
		pet= Article.objects.all().filter(user_id=user)
	else:
		posts = current_user.posts.all()# mostrar todos los post que el usuario ha hecho
		user = current_user
		userId= request.user.id
		pet = Article.objects.all().filter(user_id=userId)
		print(pet)
	return render(request, 'social/profile.html', {'user':user, 'posts':posts, 'pet':pet})

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
	current_user = request.user.id
	profileId = perfil.id

	if request.method == 'POST':
		formulario_edit = EditForm(data=request.POST, instance=perfil, files=request.FILES)  #conjunto de datos a grabar, mediante la instancia del objeto
		data = request.POST
		files = request.FILES

		if formulario_edit.is_bound == True and profileId == current_user:
			formulario_edit.save()
			messages.success(request, 'Foto de perfil editada')
			print('TRUE')
			print(data)
			return redirect('profile')
		else:
			print('El usuario no tiene permisos para editar')
	return render(request, 'social/editar.html', datos)

def eliminarpost(req):
	return None

