from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^registrarUsuario/', registrarUsuario),
    url(r'^registrarPelicula/', registrarPelicula),
    url(r'^agregarResena/', agregarResena),
    url(r'^obtenerUsuario/', obtenerUsuario),
    url(r'^obtenerPeliculas/', obtenerPeliculas),
    url(r'^obtenerPelicula/', obtenerPelicula),
    url(r'^modificarPelicula/', modificarPelicula),
    url(r'^eliminarPelicula/', eliminarPelicula),
    url(r'^obtenerResenas/', obtenerResenas),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

