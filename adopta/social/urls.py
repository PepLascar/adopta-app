from django.contrib.auth import logout
from django.urls import path
from social import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
	path('feed/', views.feed, name='feed'),
	path('profile/', views.profile, name='profile'),
	path('petProfile/', views.petProfile, name='petProfile'),
	path('profile/<str:username>/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
	path('login/', LoginView.as_view(template_name='social/login.html'), name='login'),
	path('logout/', LogoutView.as_view(template_name='social/logout.html'), name='logout'),
    path('post/', views.post, name='post'),
    path('follow/<str:username>/', views.follow, name='follow'),
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
    path('editProfile/<pk>', views.editProfile, name='editProfile'),
    path('eliminarpost/<pk>', views.eliminarpost, name='eliminarpost')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
