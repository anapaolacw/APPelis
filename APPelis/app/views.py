from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
#Imports para la comunicación con el servidor
import requests
from APPelis.settings import SERVER_URL, SERVER_URL_MEDIA

#Import para encriptar las contrasenas
import crypt

from app.models import *
""" 
    METODOS DE USUARIO
        1. iniciar
        2. registrar
        3. cerrar
    METODOS DE PELICULA
        1. detallePelicula
        2. agregarPelicula
        3. verPeliculas
        4. eliminarPelicula
        5. modificarPelicula
    METODOS DE RESENA
        1. agregarResena
    OTROS METODOS
        1. encriptarContrasena
        2. serverEnviar
"""

""" Metodo home
    Redirige a la plantilla base
"""
def home(request):
    return render(request, "base.html")

""" Metodo iniciar
    GET
        Si no hay datos de sesion, Muestra la plantilla de inicio de sesion.
        Si hay datos de sesion redirigue a la pagina principal.
    POST
        Obtiene los datos del formulario y hace una llamada al servidor para
        verificar los datos ingresados y poder iniciar sesion. Guarda los datos
        de la sesion
"""
@csrf_exempt
def iniciar(request):
    if request.method == 'GET':
        if request.session.get('logueado',None): 
            print("Ya estaba logueado", request.session['id'], ": ", request.session['correo'])
            return redirect("/peliculas/")
        else:
            return render(request, 'inicio.html')

    elif request.method == 'POST':
        correoIngresado = request.POST.get('correo','') 
        contrasenaIngresada = encriptarContrasena(request.POST.get('contrasena',''))
        if not correoIngresado or not contrasenaIngresada:
            error = 'Correo o contrasena vacios'
            return render('inicio.html',{'error':error}) 
        try:
            data = {'correo': correoIngresado} 
            respuesta = serverEnviar("", data, "/obtenerUsuario/", 1)
            
            if (respuesta['tipo'] == 1):
                usuario = respuesta['usuario']
                mensaje = 'Datos de usuario validos'
                if (usuario['contrasena'] == contrasenaIngresada):
                    request.session['logueado'] = True
                    request.session['correo'] = usuario['correo']
                    request.session['id'] = usuario['idUsuario']
                    return redirect("/peliculas/")
                else:
                    return render(request, 'inicio.html', {'error':'Contrasena incorrecta', 'status': 0})
                return render(request, 'inicio.html')
            else:
                return render(request, 'inicio.html', {'error':'Usuario inexistente', 'status': 0})
        except Exception as e: 
            print (e)
            return render(request, 'inicio.html',{'error':'Correo o contrasena invalidos '})

""" Metodo registrar
    GET
        Muestra la plantilla de registro de usuario.
    POST
        Obtiene los datos del formulario y hace una llamada al servidor para
        guardarlo en la base de datos. Redirigue a la pagina de inicio de sesion.
"""
@csrf_exempt
def registrar(request):
    if request.method == 'GET':
        return render_to_response('registro.html')

    elif request.method == 'POST':
        nombre = request.POST.get('nombre', '')
        contrasena = encriptarContrasena(request.POST.get('contrasena', ''))
        correo = request.POST.get('correo', '')
        data = {'nombre': nombre, 'contrasena': contrasena, 'correo': correo}
        respuesta = serverEnviar("", data, "/registrarUsuario/", 0)
        if respuesta != "error":
            if (respuesta['tipo'] == 1):
                mensaje = 'Datos de usuario validos'
                #request.session['id'] = usuario.id
                return render(request, 'inicio.html')
            else:
                print("Error: ", respuesta['mensaje'])
                return render(request, 'registro.html', {'error':'Error al registrar usuario', 'status': 0})
        else:
            print("Error: no hubo respuesta del servidor")
            return render(request, 'registro.html', {'error':'Error al registrar usuario', 'status': 0})
    return redirect("/home")

""" Metodo detallePelicula
    Accede al servidor para obtener los datos de pelicula seleccionada  
    y de las resenas que tiene.
"""
def detallePelicula(request, idPelicula):
    if request.method == 'GET':
        data = {'idPelicula': int(idPelicula)}
        print("request", request.session['logueado'])
        if request.session['logueado'] == True:
            plantilla = 'detalles.html'
        else:
            plantilla = 'detallesSinIniciar.html'
        respuesta = serverEnviar("", data, "/obtenerPelicula/", 1)
        if respuesta != "error":
            if (respuesta['tipo'] == 1):
                pelicula = respuesta['pelicula']
                try:
                    respuestaR = serverEnviar("", data, "/obtenerResenas/", 1)
                    print("R:", respuestaR)
                    if respuestaR != "error":
                        if (respuestaR['tipo'] == 1):
                            resenas = respuestaR['resenas']
                            return render(request, plantilla, {'pelicula': pelicula, 'resenas': resenas, 'logueado': request.session['logueado']})
                    return render(request, plantilla,{'pelicula': pelicula, 'resenas': []})
                except Exception as e:
                    print("Error", e)
                    return render(request, plantilla,{'pelicula': pelicula, 'resenas': []})
        print("Error")
        return render(request, plantilla, {'error':'Pelicula invalida', 'status': 0})

""" Metodo agregarPelicula
    GET
        Redirigue a la plantilla para agregar una pelicula.
    POST
        Accede al servidor proporcionandole los datos ingresados para
        poder guardar un registro de Pelicula en la base de datos.
""" 
@csrf_exempt
def agregarPelicula(request):
    if request.method == 'GET':
        return render_to_response('agregarPelicula.html')

    elif request.method == 'POST':
        sinopsis = request.POST.get('sinopsis', '')
        titulo = request.POST.get('titulo', '')
        fechaEstreno = request.POST.get('fechaEstreno', '')
        try:
            poster = request.FILES['poster']
        except Exception as a:
            print("Error ", a)
        files = {'poster': poster}
        data = {'sinopsis': sinopsis, 'titulo': titulo, 'fechaEstreno': fechaEstreno}
        respuesta = serverEnviar(files, data, "/registrarPelicula/", 0)
        if respuesta != "error":
            if (respuesta['tipo'] == 1):
                mensaje = 'Datos de pelicula validos'
                pelicula = Pelicula(poster = poster)
                pelicula.save()
                print("Guardado en esta bd")
                return redirect("/peliculas/")
            else:
                return render(request, 'agregarPelicula.html', {'error':'Error al registrar pelicula', 'status': 0})
        else:
            return render(request, 'agregarPelicula.html', {'error':'Error al registrar pelicula', 'status': 0})

""" Metodo verPelicula
    Accede al servidor para obtener todas las peliculas y mostralas
    en la plantilla correspondiente.
""" 
def verPeliculas(request):
    respuesta = serverEnviar("", "", "/obtenerPeliculas/", 1)

    if (respuesta != "error"):
        if (respuesta['tipo'] == 1):
            peliculas = respuesta['peliculas']    
            for peli in peliculas:
                print("P: ",peli['poster'])
            print("Valor logueado ")
            print(request.session['logueado'])
            if request.session['logueado'] == True:
                print("Estaba alguien")
                return render(request, 'peliculas.html',{'peliculas': peliculas})
            else:
                return render(request, 'base.html',{'peliculas': peliculas})
        else:
            if request.session['logueado'] == True:
                print("Estaba alguien")
                return render(request, 'peliculas.html',{'peliculas': None})
            else:
                return render(request, 'base.html',{'peliculas': None})
    else:
        if request.session['logueado'] == True:
            print("Estaba alguien")
            return render(request, 'peliculas.html',{'peliculas': None})
        else:
            return render(request, 'base.html',{'peliculas': None})

""" Metodo eliminarPelicula
    Accede al ser para eliminar el registro de Pelicula seleccionado.
"""
@csrf_exempt
def eliminarPelicula(request, idPelicula):
    data = {'idPelicula': int(idPelicula)}
    respuesta = serverEnviar("", data, "/eliminarPelicula/", 0)
    if(respuesta !="error"):
        if (respuesta['tipo'] == 1):
            return redirect("/peliculas/")
        else:
            respuestaObtener = serverEnviar("", data, "/obtenerPelicula/", 1)
            pelicula = respuestaObtener['pelicula']
            return render(request, 'detalles.html', {'pelicula': respuestaObtener['pelicula'], 'error':respuesta['mensaje'], 'status': 0})
    else:
        respuestaObtener = serverEnviar("", data, "/obtenerPelicula/", 1)
        pelicula = respuestaObtener['pelicula']
        return render(request, 'detalles.html',{'pelicula': pelicula, 'error': "No se pudo eliminar"})

""" Metodo modificarPelicula
    GET
        Obtiene los datos de la Pelicula para mostrarlos en la plantilla.
    POST
        Accede al servidor para actualizar los valores de la Pelicula.
"""
@csrf_exempt
def modificarPelicula(request, idPelicula):
    data = {'idPelicula': int(idPelicula)}
    respuesta = serverEnviar("", data, "/obtenerPelicula/", 1)
    if request.method == 'GET':
        if(respuesta != "error"):
            if (respuesta['tipo'] == 1):
                pelicula = respuesta['pelicula']
                titulo = pelicula['titulo']
                sinopsis = pelicula['sinopsis']
                idPelicula = pelicula['id']
                poster = pelicula['poster']
                fecha = pelicula['fechaEstreno']
                fechaEstreno = fecha[0:4]+ "-" + fecha[5:7] + "-" +fecha[8:10]
                valores={'titulo':titulo, 'sinopsis':sinopsis, 'poster':poster, 'fechaEstreno':fechaEstreno}
                return render_to_response('modificarPelicula.html', {'valores':valores, 'idPelicula':idPelicula})
        return render_to_response('modificarPelicula.html', {'valores':{}, 'idPelicula':idPelicula})

    elif request.method == 'POST':
        sinopsis = request.POST.get('sinopsis', '')
        titulo = request.POST.get('titulo', '')
        fechaEstreno = request.POST.get('fechaEstreno', '')
        poster = request.FILES['poster']
        files = {'poster': poster}
        data = {'idPelicula': idPelicula, 'sinopsis': sinopsis, 'titulo': titulo, 'fechaEstreno': fechaEstreno}
        respuesta = serverEnviar(files, data, "/modificarPelicula/", 0)
        if respuesta != "error":
            if (respuesta['tipo'] == 1):
                mensaje = 'Datos de pelicula validos'
                return redirect("/peliculas/")
            else:
                return render(request, 'agregarPelicula.html', {'error':'Error al registrar pelicula', 'status': 0})
        else:
            return render(request, 'agregarPelicula.html', {'error':'Error al registrar pelicula', 'status': 0})

""" Metodo agregarResena
    GET
        Muestra los detaller de la pelicula seleccionada y un formulario para
        ingresar una resena.
    POST
        Accede al servidor para guardar una nueva resena de la pelicula.
""" 
@csrf_exempt 
def agregarResena(request, idPelicula):
    if request.method == 'GET':
        data = {'idPelicula': int(idPelicula)}
        respuesta = serverEnviar("", data, "/obtenerPelicula/", 1)
        if respuesta != "error":
            if (respuesta['tipo'] == 1):
                pelicula = respuesta['pelicula']
                return render(request, 'resena.html', {'pelicula': pelicula})
        return render(request, 'detalles.html', {'error':'Pelicula invalida', 'status': 0})

    elif request.method == 'POST':
        resena = request.POST.get('resena')
        data = {'resena': resena, 'idPelicula': int(idPelicula), 'idUsuario': request.session['id']}
        respuesta = serverEnviar("", data, "/agregarResena/", 0)
        if respuesta != "error":
            if (respuesta['tipo'] == 1):
                return redirect("/pelicula/" +idPelicula)
        data = {'idPelicula': int(idPelicula)}
        respuestaP = serverEnviar("", data, "/obtenerPelicula/", 1)
        if respuestaP != "error":
            if (respuestaP['tipo'] == 1):
                pelicula = respuestaP['pelicula']
                return render(request, 'resena.html', {'pelicula': pelicula, 'error': 'Error al agregar resena'})
        return redirect("/peliculas/")

""" Metodo cerrar
    Se cambian los datos de la sesion para cerrar sesion.
"""
def cerrar(request):
    request.session['logueado'] = False
    print("Sesion cerrada")
    return redirect("/home")

""" Metodo encriptarContrasena
    Metodo para encriptar la contrasena.
"""  
def encriptarContrasena(contrasena):
    passw = crypt.crypt(contrasena, 'salt')
    return passw

""" Metodo serverEnviar
    Metodo que realiza la peticion al servidor y proporciona headers, data y 
    archivos, segun se requiera
"""
def serverEnviar(files, data, direccionServer, tipoPeticion):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)', 'Media-Type':'multipart/form-data'}
    print("Peticion ", direccionServer)
    try:
        if (tipoPeticion == 0):
            print("es post")
            res = (requests.post(SERVER_URL+direccionServer, headers = headers , files = files, data = data))
            print("res", res)
            r = res.json()            
        else:
            print("es get")
            r = requests.post(SERVER_URL+direccionServer, headers = headers , data = data).json()
        return r
    except Exception as e:
        print("Error al enviar", e)
        return "error"