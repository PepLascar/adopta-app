from django.urls import path
from social import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
	path('feed/', views.feed, name='feed'),
	path('profile/', views.profile, name='profile'),
	path('petProfile/<int:id>', views.petProfile, name='petProfile'),
	path('profile/<str:username>/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
	path('login/', LoginView.as_view(template_name='social/login.html'), name='login'),
	path('logout/', LogoutView.as_view(template_name='social/logout.html'), name='logout'),
    path('mail/<id>', views.mail, name='mail'),
    path('inbox/<id>', views.inbox, name='inbox'),
    path('chats/', views.chats, name='chats'),
    path('follow/<str:username>/', views.follow, name='follow'),
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
    path('editProfile/<pk>', views.editProfile, name='editProfile'),
    path('eliminarpost/<pk>', views.eliminarpost, name='eliminarpost')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)