from django.contrib import admin
from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('donar/', views.donar, name="donar"),
    path('listar/', views.listar, name="listar"),
    path('crear/', views.crear, name="crear"),
    path('editar/<pk>', views.editar, name="editar"),
    path('eliminar/<pk>', views.eliminar, name="eliminar")
]

#para las imágenes
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)