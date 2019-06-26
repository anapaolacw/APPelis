"""APPelis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from app.views import *

#imports para imagenes
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^home/', verPeliculas),
    url(r'^iniciar/', iniciar),
    url(r'^registrar/', registrar),
    url(r'^peliculas/', verPeliculas),
    url(r'^agregarPelicula/', agregarPelicula),
    url(r'^modificarPelicula/(?P<idPelicula>\d+)/$', modificarPelicula),
    url(r'^eliminarPelicula/(?P<idPelicula>\d+)/$', eliminarPelicula),
    url(r'^agregarResena/(?P<idPelicula>\d+)/$', agregarResena),
    url(r'^pelicula/(?P<idPelicula>\d+)/$', detallePelicula),
    url(r'^cerrar/', cerrar),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

