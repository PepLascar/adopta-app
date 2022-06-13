from django.contrib import admin
from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.listar, name="listar"),
    path('stats/', views.stats, name="stats"),
    path('crear/', views.crear, name="crear"),
    path('editPet/<pk>', views.editPet, name="editPet"),
    path('eliminar/<pk>', views.eliminar, name="eliminar")
]

#para las imágenes
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)