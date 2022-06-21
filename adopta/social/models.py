from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='miki.png')

	def __str__(self):
		return f'Perfil de {self.user.username}'

	def following(self):
		user_ids = Relationship.objects.filter(from_user=self.user).values_list('to_user_id', flat=True)
		return User.objects.filter(id__in=user_ids)

	def followers(self):
		user_ids = Relationship.objects.filter(to_user=self.user).values_list('from_user_id', flat=True)
		return User.objects.filter(id__in=user_ids)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    timestamp = models.DateTimeField(default=timezone.now)#momento en que el post ha sido creado
    content = models.TextField()

    class Meta: #definir como quiero que se comporte una clase
        ordering = ['-timestamp']  #mostrar en orden descendente

    def __str__(self):  #si lo quito se refleja directamente como lo muestra en el admin
        return f'{self.user.username}: {self.content}'  #mostrar el contenido vinculado a un usuario, represetarlo en string

class Inbox(models.Model):
	sender  = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
	to_user = models.ForeignKey(User, related_name='reciever', on_delete=models.CASCADE)
	content = models.TextField(default=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Creado el')    #related name cambia el nombre en la template 

	class Meta:
		ordering = ['-created_at']

class Relationship(models.Model):
	from_user = models.ForeignKey(User, related_name='relationships', on_delete=models.CASCADE)
	to_user = models.ForeignKey(User, related_name='related_to', on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.from_user} to {self.to_user}'

	class Meta:
		indexes = [
		models.Index(fields=['from_user', 'to_user',]),
		]


"""
Trabajando con imágenes.
- setiar ImageField en el modelo con una imágen default.
- definir MEDIA_URL en SETTINGS  -  url en la cual se va a acceder a las imagenes
- MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
-- acceder desde las template al modelo donde se encuentran las imagénes
- En las URL definir -> if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    Setiar una imagen default: 

Cargar CSS correctamente vía static hacia el layout

Importe de vistas automáticas de login/logout
en URL from django.contrib.auth.views import LoginView, LogoutView
luego crear su respectivo path

Para que cada vez que se cree un usuario se cree un perfil:
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    post_save.connect(create_profile, sender=User)

Crear señales
    Para que el post se vincule al usuario

Configurar cosas propias del usuario
"""
