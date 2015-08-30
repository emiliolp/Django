from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from usuario.models import Usuario, PerfilUsuario, PeticionAmistad, Comentario, Voto
from usuario.forms import UserForm, PerfilForm, PeticionAmistadForm, ComentarioForm, VotoForm
from diario.models import *
from django.db.models import Avg,Max,Min,Count

# Index usuario logueado
def indexUsuario (request):
	usuarioLogueado = Usuario.objects.get (pk = request.user.id)
	if usuarioLogueado.perfilActivo == 'Real':
		comentarios = usuarioLogueado.perfilReal.Comentario_PerfilUsuario.filter (padre = 'True')
		perfil=usuarioLogueado.perfilReal
	else:
		comentarios = usuarioLogueado.perfilFalso.Comentario_PerfilUsuario.filter (padre = 'True')
		perfil=usuarioLogueado.perfilFalso
	numAmigos=perfil.amigos.count()
	context = {'comentarios': comentarios,'perfil':perfil,'numAmigos':numAmigos}
	return render (request, 'usuario/index_usuario.html', context)

# Registrar nuevo usuario
def nuevoUsuario (request):
	if request.method == 'POST':
		form = UserForm (request.POST, request.FILES)
		if form.is_valid ():
			form.save ()
			user = Usuario.objects.get (username = request.POST ['username'])
			# Crea los diarios y la agenda del usuario
			agenda = Agenda.objects.create (usuario = user)
			diarioPersonal = DiarioPersonal.objects.create (usuario = user)
			diarioPensamientos = DiarioPensamientos.objects.create (usuario = user)
			# Despues de registrar al nuevo usuario, lo loguea automaticamente
			nombre = request.POST ['username']
			passwd = request.POST ['password1']
			usuario = authenticate (username = nombre, password = passwd)
			login (request, usuario)
			# Despues de loguear al nuevo usuario, lo lleva a crear su perfil real
			return redirect ('/usuario/crear-perfil-real')
	else:
		form = UserForm ()
	context = {'form': form}
	return render (request, 'usuario/nuevo_usuario.html', context)

# Crear perfil real
def crearPerfilReal (request):
	usuarioLogueado = Usuario.objects.get (username = request.user.username)
	perfilReal = usuarioLogueado.perfilReal
	if request.method == 'POST':
		form = PerfilForm (request.POST, request.FILES, instance = perfilReal)
		if form.is_valid ():
			form.save ()
			# Despues de crear el perfil real, lleva al usuario a crear su perfil falso
			return redirect ('/usuario/crear-perfil-falso')
	else:
		form = PerfilForm ()
	context = {'form': form, 'perfil': perfilReal}
	return render (request, 'usuario/crear_perfil.html', context)

# Crear perfil falso
def crearPerfilFalso (request):
	usuarioLogueado = Usuario.objects.get (username = request.user.username)
	perfilFalso = usuarioLogueado.perfilFalso
	if request.method == 'POST':
		form = PerfilForm (request.POST, request.FILES, instance = perfilFalso)
		if form.is_valid ():
			form.save ()
			# Despues de crear el perfil falso, lleva al usuario al index
			return redirect ('/usuario/')
	else:
		form = PerfilForm ()
	context = {'form': form, 'perfil': perfilFalso}
	return render (request, 'usuario/crear_perfil.html', context)

# Detalles perfil
def detallesPerfil (request, usuario_id,latitud_value,longitud_value):
	usuarioLogueado = Usuario.objects.get (username = request.user.username)
	usuario = Usuario.objects.get (pk = usuario_id)
	user=usuario
	# Obtiene ultimo pensamiento
	diario_usuario=DiarioPensamientos.objects.get(usuario=user)
	ids_entrada=EntradaDiarioPensamientos.objects.filter(diarioPensamientos=diario_usuario).aggregate(Max('id')).values()
	id_entrada=ids_entrada[0]
	if id_entrada>0:
		ultimaEntrada=EntradaDiarioPensamientos.objects.get(id=id_entrada)
		#ultimaEntradaFinal=ultimaEntrada.contenido
	else:
		ultimaEntrada='...'
	# Obtiene el perfil activo del usuario objetivo para poder mostrar su informacion
	if usuario.perfilActivo == 'Real':
		perfil = usuario.perfilReal
	else:
		perfil = usuario.perfilFalso
	# Obtiene los amigos del perfil activo del usuario logueado para comprobar si el usuario objetivo es o no su amigo
	if usuarioLogueado.perfilActivo == 'Real':
		perfilLogueado = usuarioLogueado.perfilReal
	else:
		perfilLogueado = usuarioLogueado.perfilFalso
	amigosLogueado = perfilLogueado.amigos.all ()

	if not amigosLogueado.filter (pk = perfil.id).exists ():
		amigosLogueado = None
	numAmigos=perfil.amigos.count()

	PerfilUsuario.objects.filter(id=perfilLogueado.id).update(latitud=latitud_value)
	PerfilUsuario.objects.filter(id=perfilLogueado.id).update(longitud=longitud_value)
	#Evita que salga la alarma de que no es amigo el perfil actual
	amigo=True
	context = {'perfilLogueado': perfil, 'perfil':perfil,'usuario': usuario, 'amigosLogueado': amigosLogueado,'numAmigos':numAmigos,'ultimoPensamiento':ultimaEntrada, 'amigo':amigo}
	return render (request, 'usuario/detalles_perfil.html', context)

# Ver perfil
def verPerfil(request,perfil_id):
	usuarioLogueado = Usuario.objects.get (username = request.user.username)
	if usuarioLogueado.perfilActivo == 'Real':
		perfilLogueado = usuarioLogueado.perfilReal
	else:
		perfilLogueado = usuarioLogueado.perfilFalso
	numAmigos=perfilLogueado.amigos.count()
	perfil=PerfilUsuario.objects.get(pk=perfil_id)

	# Comprueba si el perfil a visitar esta en la lista de amigos del perfil logueado para proporcionar las opciones adecuadas
	if perfil in perfilLogueado.amigos.all():
		amigo = True
	else:
		amigo = False
	context={'perfilLogueado': perfil, 'perfil': perfilLogueado, 'amigo': amigo, 'numAmigos': numAmigos}
	return render(request,'usuario/detalles_perfil.html',context)

# Editar perfil
def editarPerfil (request, perfil_id):
	perfil = PerfilUsuario.objects.get (pk = perfil_id)
	if request.method == 'POST':
		form = PerfilForm (request.POST, request.FILES,instance = perfil)
		if form.is_valid ():
			form.save ()
			return redirect ('/usuario/')
	else:
		form = PerfilForm (instance = perfil)
	numAmigos=perfil.amigos.count()
	context = {'form': form,'perfil':perfil,numAmigos:'numAmigos'}
	return render (request, 'usuario/editar_perfil.html', context)

# Mostrar gente cerca
def mostrarGenteCerca(request,usuario_id,latitud_value,longitud_value):
	cercanoList=[]
	perfilesActivos=[]
	usuarios=Usuario.objects.all()
	for user in usuarios:
		if user.perfilActivo == 'Real':
			perfilesActivos.append(user.perfilReal)
		else:
			perfilesActivos.append(user.perfilFalso)

	#Guardamos latitud y longitud a la base de datos

	#Buscamos perfil activo del usuario pasado
	usuario=Usuario.objects.get(pk=usuario_id)
	if usuario.perfilActivo == 'Real':
		perfilUsuario=usuario.perfilReal
	else:
		perfilUsuario=usuario.perfilFalso

	PerfilUsuario.objects.filter(id=perfilUsuario.id).update(latitud=latitud_value)
	PerfilUsuario.objects.filter(id=perfilUsuario.id).update(longitud=longitud_value)
	#perfilUsuario.latitud=latitud_value
	#perfilUsuario.longitud=longitud_value
	#perfilUsuario.save()

	#Guardamos los usuarios cercanos en el vector
	for perfil in perfilesActivos:
		distancia=perfil.longitud-float(perfilUsuario.longitud)
		distanciaKm=distancia*111.12
		if distanciaKm <= 5 and distanciaKm >= -5 and perfil.nombre!=perfilUsuario.nombre:
			cercanoList.append(perfil)
	numAmigos=perfilUsuario.amigos.count()
	friends=perfilUsuario.amigos.all()

	context={'perfil':perfilUsuario,'numAmigos':numAmigos,'cercanoList':cercanoList,'amigos':friends}
	return render(request,'usuario/gente_cerca.html',context)

# Cambiar perfil
def cambiarPerfil (request):
	usuarioLogueado = Usuario.objects.get (username = request.user.username)
	if usuarioLogueado.perfilActivo == 'Real':
		usuarioLogueado.perfilActivo = 'Falso'
	else:
		usuarioLogueado.perfilActivo = 'Real'
	usuarioLogueado.save ()
	return redirect ('/usuario/')

# Buscar perfil
def buscar (request):
	perfiles=PerfilUsuario.objects.all()
	context={'perfiles':perfiles}
	return render(request,'usuario/buscarPerfil.html',context)

# Buscar usuarios (barra de navegacion)
def buscarUsuario (request):
	usuarioLogueado = Usuario.objects.get (pk = request.user.id)

	if usuarioLogueado.perfilActivo == 'Real':
		perfil=usuarioLogueado.perfilReal
	else:
		perfil=usuarioLogueado.perfilFalso
	numAmigos=perfil.amigos.count()
	if 'name' in request.GET and request.GET ['name']:
		name = request.GET ['name']
		perfiles = PerfilUsuario.objects.filter (nombre = name).exclude (pk = perfil.id)
		context = {'perfiles': perfiles,'perfil':perfil,'numAmigos':numAmigos}
		return render (request, 'usuario/buscar_usuario.html', context)
	else:
		return render (request, 'usuario/no_busqueda.html')

# Enviar peticion de amistad
def enviarPeticionAmistad (request, perfil_id):
	perfilObjetivo = PerfilUsuario.objects.get (pk = perfil_id)
	usuarioLogueado = Usuario.objects.get (username = request.user.username)

	if usuarioLogueado.perfilActivo == 'Real':
		perfil = usuarioLogueado.perfilReal
	else:
		perfil = usuarioLogueado.perfilFalso
	numAmigos=perfil.amigos.count()
	if request.method == 'POST':
		peticion = PeticionAmistad.objects.create (perfil_solicitante = perfil.nombre, perfil_objetivo = perfilObjetivo)
		form = PeticionAmistadForm (request.POST, instance = peticion)
		if form.is_valid ():
			form.save ()
			return redirect ('/usuario/')
	else:
		# Comprueba si el usuario ya a enviado una solicitud de amistad al perfil indicado
		peticiones = PeticionAmistad.objects.filter (perfil_objetivo = perfilObjetivo)
		if peticiones.filter (perfil_solicitante = perfil.nombre).exists ():
			context = {'perfil': perfilObjetivo}
			return render (request, 'usuario/peticion_ya_enviada.html', context)
		else:
			form = PeticionAmistadForm ()
			context = {'form': form,'perfil':perfil,'numAmigos':numAmigos}
			return render (request, 'usuario/nueva_peticion_amistad.html', context)

def dejarSeguir (request, perfil_id):
	perfilAmigo = PerfilUsuario.objects.get (pk = perfil_id)
	usuarioLogueado = Usuario.objects.get (username = request.user.username)
	if usuarioLogueado.perfilActivo == 'Real':
		perfilLogueado = usuarioLogueado.perfilReal
	else:
		perfilLogueado = usuarioLogueado.perfilFalso
	perfilLogueado.amigos.remove (perfilAmigo)
	perfilAmigo.amigos.remove (perfilLogueado)
	#entradas agenda
	agenda_usuario = Agenda.objects.get (usuario = usuarioLogueado)
	entradas = EntradaAgenda.objects.filter (agenda = agenda_usuario)
	#usuario logueado
	if usuarioLogueado.perfilActivo == 'Real':
		perfil=usuarioLogueado.perfilReal
	else:
		perfil=usuarioLogueado.perfilFalso
	numAmigos=perfil.amigos.count()
	context = {'perfilAmigo': perfilAmigo,'entradas':entradas,'perfil':perfil,'numAmigos':numAmigos}
	return render (request, 'usuario/dejar_seguir.html', context)

# Ver peticiones de amistad pendientes
def verPeticionesAmistad (request, usuario_id):
	usuarioLogueado = Usuario.objects.get (pk = usuario_id)
	if usuarioLogueado.perfilActivo == 'Real':
		perfil = usuarioLogueado.perfilReal
	else:
		perfil = usuarioLogueado.perfilFalso
	numAmigos=perfil.amigos.count()
	peticiones = PeticionAmistad.objects.filter (perfil_objetivo = perfil)
	
	context = {'peticiones': peticiones,'perfil':perfil,'numAmigos':numAmigos}
	return render (request, 'usuario/ver_peticiones_amistad.html', context)

# Detalles de una peticion de amistad
def detallesPeticionAmistad (request, peticion_id):
	usuarioLogueado = Usuario.objects.get (pk = request.user.id)
	if usuarioLogueado.perfilActivo == 'Real':
		perfil=usuarioLogueado.perfilReal
	else:
		perfil=usuarioLogueado.perfilFalso
	numAmigos=perfil.amigos.count()
	peticion = PeticionAmistad.objects.get (pk = peticion_id)
	
	context = {'peticion': peticion,'perfil':perfil,'numAmigos':numAmigos}
	return render (request, 'usuario/detalles_peticion_amistad.html', context)

# Aceptar peticion de amistad
def aceptarPeticionAmistad (request, peticion_id):
	usuarioLogueado = Usuario.objects.get (pk = request.user.id)
	if usuarioLogueado.perfilActivo == 'Real':
		perfil=usuarioLogueado.perfilReal
	else:
		perfil=usuarioLogueado.perfilFalso
	numAmigos=perfil.amigos.count()
	peticion = PeticionAmistad.objects.get (pk = peticion_id)
	perfilSolicitante = PerfilUsuario.objects.get (nombre = peticion.perfil_solicitante)
	perfilObjetivo = peticion.perfil_objetivo
	perfilSolicitante.amigos.add (peticion.perfil_objetivo)
	perfilObjetivo.amigos.add (perfilSolicitante)
	peticion.delete ()
	
	context = {'perfilSolicitante': perfilSolicitante,'perfil':perfil,'numAmigos':numAmigos}
	return render (request, 'usuario/aceptar_peticion_amistad.html', context)

# Rechazar peticion de amistad
def rechazarPeticionAmistad (request, peticion_id):
	usuarioLogueado = Usuario.objects.get (pk = request.user.id)
	if usuarioLogueado.perfilActivo == 'Real':
		perfil=usuarioLogueado.perfilReal
	else:
		perfil=usuarioLogueado.perfilFalso
	numAmigos=perfil.amigos.count()
	peticion = PeticionAmistad.objects.get (pk = peticion_id)
	peticion.delete ()
	
	context = {'peticion': peticion,'perfil':perfil,'numAmigos':numAmigos}
	return render (request, 'usuario/rechazar_peticion_amistad.html', context)

# Ver amigos
def verAmigos (request, perfil_id):
	usuarioLogueado = Usuario.objects.get (pk = request.user.id)
	if usuarioLogueado.perfilActivo == 'Real':
		perfil=usuarioLogueado.perfilReal
	else:
		perfil=usuarioLogueado.perfilFalso
	numAmigos=perfil.amigos.count()
	perfil = PerfilUsuario.objects.get (pk = perfil_id)
	amigos = perfil.amigos.all ()
	
	context = {'amigos': amigos,'perfil':perfil,'numAmigos':numAmigos}
	return render (request, 'usuario/ver_amigos.html', context)

# Nuevo comentario
def nuevoComentario (request, perfil_id):
	userLoged=Usuario.objects.get(username=request.user.username)
	if userLoged.perfilActivo=='Real':
		perfilLoged=userLoged.perfilReal
	else:
		perfilLoged=userLoged.perfilFalso
	numAmigos=perfilLoged.amigos.count()

	perfilUsuario = PerfilUsuario.objects.get (pk = perfil_id)
	if request.method == 'POST':
		usuarioLogueado = Usuario.objects.get (username = request.user.username)
		if usuarioLogueado.perfilActivo == 'Real':
			perfilLogueado = usuarioLogueado.perfilReal
		else:
			perfilLogueado = usuarioLogueado.perfilFalso
		#numAmigos=perfil.amigos.count()
		comentario = Comentario.objects.create (perfilReceptor = perfilUsuario, perfilEmisor = perfilLogueado.nombre, padre = 'True')
		form = ComentarioForm (request.POST, instance = comentario)
		if form.is_valid ():
			form.save ()
			return redirect ('/usuario/')
	else:
		form = ComentarioForm ()
	context = {'form': form,'perfil':perfilLoged,'numAmigos':numAmigos}
	return render (request, 'usuario/nuevo_comentario.html', context)

# Detalles comentario
def detallesComentario (request, comentario_id):
	comentario = Comentario.objects.get (pk = comentario_id)
	comentarios = comentario.comentario.all ()
	#usuario logueado
	usuarioLogueado = Usuario.objects.get (pk = request.user.id)
	if usuarioLogueado.perfilActivo == 'Real':
		perfil=usuarioLogueado.perfilReal
	else:
		perfil=usuarioLogueado.perfilFalso
	numAmigos=perfil.amigos.count()
	context = {'comentario': comentario, 'comentarios': comentarios,'perfil':perfil,'numAmigos':numAmigos}
	return render (request, 'usuario/detalles_comentario.html', context)

# Hacer comentario
def hacerComentario (request, comentario_id):
	#usuario logueado
	usuarioLogueado = Usuario.objects.get (pk = request.user.id)
	if usuarioLogueado.perfilActivo == 'Real':
		perfil=usuarioLogueado.perfilReal
	else:
		perfil=usuarioLogueado.perfilFalso
	numAmigos=perfil.amigos.count()

	if request.method == 'POST':
		usuarioLogueado = Usuario.objects.get (username = request.user.username)
		if usuarioLogueado.perfilActivo == 'Real':
			perfilLogueado = usuarioLogueado.perfilReal
		else:
			perfilLogueado = usuarioLogueado.perfilFalso
		# Obtiene el comentario sobre el que se va a realizar el comentario
		comentarioObjetivo = Comentario.objects.get (pk = comentario_id)
		comentario = Comentario.objects.create (perfilReceptor = comentarioObjetivo.perfilReceptor, perfilEmisor = perfilLogueado.nombre, padre = 'False')
		comentarioObjetivo.comentario.add (comentario)
		form = ComentarioForm (request.POST, instance = comentario)
		if form.is_valid ():
			form.save ()
			return redirect ('/usuario/')
	else:
		form = ComentarioForm ()
	context = {'form': form,'perfil':perfil,'numAmigos':numAmigos}
	return render (request, 'usuario/nuevo_comentario.html', context)

# Votar perfil
def votarPerfil (request, perfil_id):
	perfilUsuario = PerfilUsuario.objects.get (pk = perfil_id)
	usuarioLogueado = Usuario.objects.get (username = request.user.username)
	if usuarioLogueado.perfilActivo == 'Real':
		perfilLogueado = usuarioLogueado.perfilReal
	else:
		perfilLogueado = usuarioLogueado.perfilFalso
	numAmigos=perfilLogueado.amigos.count()
	if request.method == 'POST':
		voto = Voto.objects.create (perfilVotado = perfilUsuario, perfilVotante = perfilLogueado)
		form = VotoForm (request.POST, instance = voto)
		if form.is_valid ():
			form.save ()
			votos=perfilUsuario.Voto_PerfilUsuario.all()
			suma=0
			for voto in votos:
				suma=suma+voto.puntuacion
			media=suma/len(votos)
			PerfilUsuario.objects.filter(id=perfil_id).update(mediaVotos=media)
			return redirect ('/usuario/')
	else:
		form = VotoForm ()
	context = {'form': form,'perfil':perfilLogueado,'numAmigos':numAmigos}
	return render (request, 'usuario/votar_perfil.html', context)

# Login
def usuarioLogin (request):
	if request.method == 'POST':
		form = AuthenticationForm (request.POST)
		if form.is_valid:
			nombre = request.POST ['username']
			passwd = request.POST ['password']
			usuario = authenticate (username = nombre, password = passwd)
			if usuario is not None:
				if usuario.is_active:
					login (request, usuario)
					return redirect ('/usuario/')
				else:
					return render (request, 'usuario/inactivo.html')
			else:
				return render (request, 'usuario/no_usuario.html')
	else:
		form = AuthenticationForm ()
	context = {'form': form}
	return render (request, 'usuario/login.html', context)

# Logout
@login_required (login_url = '/usuario/login')
def usuarioLogout (request):
    logout (request)
    return redirect ('/')
