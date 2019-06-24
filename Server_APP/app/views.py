import os
from django.shortcuts import render
from app.models import *
from app.serializers import *
from django.http import HttpResponse, JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.conf import settings

""" 
    METODOS DE MANEJO DE USUARIO
        1. registrarUsuario 
        2. obtenerUsuario
    METODOS DE MANEJO DE PELICULA
        1. obtenerPeliculas
        2. obtenerPelicula
        3. registrarPelicula
        4. modificarPelicula
        5. eliminarPelicula
    METODOS DE MANEJO DE RESENAS
        1. obtenerResenas
        2. agregarResena
"""

""" Metodo registrarUsuario
    Obtiene los datos de la peticion para registrar un nuevo usuario
"""
@csrf_exempt
def registrarUsuario(request):
    nombre = request.POST.get("nombre", None)
    contrasena = request.POST.get("contrasena", None)
    correo = request.POST.get("correo", None)
    usuario = Usuario(nombre=nombre, contrasena=contrasena, correo=correo)
    try:
        usuario.save()
        data = {'mensaje': "Usuario registrado", 'tipo': 1}
    except Exception as e:
        data= {'mensaje': e, 'tipo': 0}
    return JsonResponse(data)

""" Metodo obtenerUsuario
    Obtiene los datos de la peticion y los usuarios de la base de datos 
    y devuelve un json con el usuario que tenga el mismo correo
"""
@csrf_exempt
def obtenerUsuario(request):
    usuarios = Usuario.objects.all()
    correo = request.POST['correo']
    for usuario in usuarios:
        if usuario.correo == correo:
            user = Usuario()
            user = usuario
        else:
            user = None
    if user:
        u ={'nombre': usuario.nombre, 'correo': usuario.correo, 'contrasena': usuario.contrasena, 'idUsuario':usuario.id}
        data = {'usuario': u, 'tipo': 1}
    else:
        data= {'usuario': None , 'tipo': 0}
    return JsonResponse(data)

""" Metodo obtenerPeliculas
    Obtiene todas las peliculas de la base de datos y las devuelve
    en un json
"""
@csrf_exempt
def obtenerPeliculas(request):
    peliculas = Pelicula.objects.all().order_by('titulo')
    if len(peliculas)==0:
        data = {'peliculas': None, 'tipo' : 0}
    else:
        listaPelis = []
        for peli in peliculas:
            anio = str(peli.fechaEstreno)[0:4]
            mes = str(peli.fechaEstreno)[5:7]
            dia = str(peli.fechaEstreno)[8:10]
            listaPelis.append({'titulo': peli.titulo, 'sinopsis': peli.sinopsis, 'poster': str(peli.poster), 'fechaEstreno': peli.fechaEstreno,'id':peli.id, 'anio': anio, 'mes': mes, 'dia': dia})
        data = {'peliculas': listaPelis, 'tipo': 1}
    return JsonResponse(data)

""" Metodo obtenerPelicula
    Obtiene la pelicula de la base de datos que coincida con el id ingresado
    y la devuelve como json
"""
@csrf_exempt
def obtenerPelicula(request):
    idPelicula = int(request.POST['idPelicula'])
    peli = Pelicula.objects.get(id = idPelicula)
    if peli != None:
        pelicula = {'titulo': peli.titulo, 'sinopsis': peli.sinopsis, 'poster': str(peli.poster), 'fechaEstreno': peli.fechaEstreno,'id':idPelicula}
        data = {'pelicula': pelicula, 'tipo': 1}    
    else:
        data = {'peliculas': None, 'tipo' : 0}
    return JsonResponse(data)

""" Metodo registrarPelicula
    Obtiene los datos de la peticion para crear un elemento Pelicula
    y guardarlo en la base de datos. Devuelve un mensaje.
"""
@csrf_exempt
def registrarPelicula(request):
    titulo = request.POST.get("titulo", None)
    sinopsis = request.POST.get("sinopsis", None)
    fechaEstreno = request.POST.get("fechaEstreno", None)
    poster = request.FILES['poster']
    pelicula = Pelicula(titulo=titulo, sinopsis=sinopsis, fechaEstreno=fechaEstreno, poster=poster)

    try:
        pelicula.save()
        data = {'mensaje': "Pelicula registrada", 'tipo': 1}
    except Exception as e:
        data= {'mensaje': e, 'tipo': 0}
    return JsonResponse(data)

""" Metodo modificarPelicula
    Obtiene los datos de la peticion para actualizar el registro de
    la base de datos de la Pelicula que coincida con el id. Devuelve
    un mensaje.
"""
@csrf_exempt
def modificarPelicula(request):
    idPelicula = request.POST.get("idPelicula", None)
    peli = Pelicula.objects.get(id = idPelicula)
    peli.titulo = request.POST.get("titulo", None)
    peli.sinopsis = request.POST.get("sinopsis", None)
    peli.fechaEstreno = request.POST.get("fechaEstreno", None)
    peli.poster = request.FILES['poster']
    try:
        peli.save()
        data = {'mensaje': "Cambios guardados", 'tipo': 1}
    except Exception as e:
        data= {'mensaje': e, 'tipo': 0}
    return JsonResponse(data)

""" Metodo eliminarPelicula
    Elimina el registro de la base de datos que coincida con el id 
    ingresado y devuelve un mensaje json.
"""
@csrf_exempt
def eliminarPelicula(request):
    idPelicula = int(request.POST['idPelicula'])
    try:
        Pelicula.objects.filter(id = idPelicula).delete()
        data= {'mensaje': "Pelicula eliminada", 'tipo': 1}
    except Exception as e:
        data = {'mensaje': e, "tipo": 0}
    return JsonResponse(data)

""" Metodo obtenerResenas
    Obtiene todas las resenas de la base de datos que pertenezcan al id 
    de la pelicula solicitada y las devuelve como json
"""
@csrf_exempt
def obtenerResenas(request):
    idPelicula = int(request.POST['idPelicula'])
    resenas = Resena.objects.filter(idPelicula = idPelicula)
    if len(resenas)==0:
        data = {'resenas': None, 'tipo' : 0}
    else:
        listaResenas = []
        for resena in resenas:
            listaResenas.append({'resena': resena.resena})
        data = {'resenas': listaResenas, 'tipo': 1}
    return JsonResponse(data)

""" Metodo agregarResena
    Obtiene los datos de la peticion para crear un elemento Resena
    y guardarlo en la base de datos. Devuelve un mensaje.
"""
@csrf_exempt
def agregarResena(request):
    resena = request.POST.get("resena", None)
    idUsuario = request.POST.get("idUsuario", None)
    idPelicula = request.POST.get("idPelicula", None)
    usuario = Usuario.objects.get(id = idUsuario)
    pelicula = Pelicula.objects.get(id = idPelicula)
    resena = Resena(resena=resena, idUsuario=usuario, idPelicula=pelicula)
    try:
        resena.save()
        data = {'mensaje': "Resena agregada", 'tipo': 1}
    except Exception as e:
        data= {'mensaje': e, 'tipo': 0}
    return JsonResponse(data)
