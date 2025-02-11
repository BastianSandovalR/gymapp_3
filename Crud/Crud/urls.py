from django.shortcuts import render # type: ignore
#from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),  # Rutas del administrador
    path('', include('gymapp.urls')),  # Redirige las rutas de la aplicación gymapp
]

# Si tienes archivos multimedia, añade esta línea
#if settings.DEBUG:
 #   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
