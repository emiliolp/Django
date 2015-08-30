from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from usuario.models import Usuario,PerfilUsuario
from diario.forms import EntradaAgendaForm, EntradaDiarioPersonalForm, EntradaDiarioPensamientosForm
from diario.models import Agenda, DiarioPersonal, DiarioPensamientos, EntradaAgenda, EntradaDiarioPersonal, EntradaDiarioPensamientos

# Ver agenda
def verAgenda (request, usuario_id):
	user = Usuario.objects.get (pk = usuario_id)
	agenda_usuario = Agenda.objects.get (usuario = user)
	entradas = EntradaAgenda.objects.filter (agenda = agenda_usuario)
	#usuario logueado
	usuarioLogueado = Usuario.objects.get (pk = request.user.id)
	if usuarioLogueado.perfilActivo == 'Real':
		perfil=usuarioLogueado.perfilReal
	else:
		perfil=usuarioLogueado.perfilFalso
	numAmigos=perfil.amigos.count()
	context = {'entradas': entradas, 'agenda': agenda_usuario,'perfil':perfil,'numAmigos':numAmigos}
	return render (request, 'diario/agenda.html', context)

# Ver diario personal
def verDiarioPersonal (request, usuario_id):
	user = Usuario.objects.get (pk = usuario_id)
	diario_usuario = DiarioPersonal.objects.get (usuario = user)
	entradas = EntradaDiarioPersonal.objects.filter (diarioPersonal = diario_usuario)
	#usuario logueado
	usuarioLogueado = Usuario.objects.get (pk = request.user.id)
	if usuarioLogueado.perfilActivo == 'Real':
		perfil=usuarioLogueado.perfilReal
	else:
		perfil=usuarioLogueado.perfilFalso
	numAmigos=perfil.amigos.count()
	context = {'entradas': entradas, 'diario': diario_usuario,'perfil':perfil,'numAmigos':numAmigos}
	return render (request, 'diario/diarioPersonal.html', context)

# Ver diario pensamientos
def verDiarioPensamientos (request, usuario_id):
	user = Usuario.objects.get (pk = usuario_id)
	diario_usuario = DiarioPensamientos.objects.get (usuario = user)
	entradas = EntradaDiarioPensamientos.objects.filter (diarioPensamientos = diario_usuario)
	#usuario logueado
	usuarioLogueado = Usuario.objects.get (pk = request.user.id)
	if usuarioLogueado.perfilActivo == 'Real':
		perfil=usuarioLogueado.perfilReal
	else:
		perfil=usuarioLogueado.perfilFalso
	numAmigos=perfil.amigos.count()
	context = {'entradas': entradas, 'diario': diario_usuario,'perfil':perfil,'numAmigos':numAmigos}
	return render (request, 'diario/diarioPensamientos.html', context)

# Agenda nueva entrada
def agendaNuevaEntrada (request, agenda_id):
	#usuario logueado
	usuarioLogueado = Usuario.objects.get (pk = request.user.id)
	if usuarioLogueado.perfilActivo == 'Real':
		perfil=usuarioLogueado.perfilReal
	else:
		perfil=usuarioLogueado.perfilFalso
	numAmigos=perfil.amigos.count()

	agenda_usuario = Agenda.objects.get (pk = agenda_id)
	if request.method == 'POST':
		entradaAgenda = EntradaAgenda.objects.create (agenda = agenda_usuario)
		form = EntradaAgendaForm (request.POST, instance = entradaAgenda)
		if form.is_valid ():
			form.save ()
			return redirect ('/usuario/')
	else:
		form = EntradaAgendaForm ()
	context = {'form': form,'perfil':perfil,'numAmigos':numAmigos}
	return render (request, 'diario/nueva_entrada.html', context)

# Diario personal nueva entrada
def diarioPersonalNuevaEntrada (request, diario_id):
	#usuario logueado
	usuarioLogueado = Usuario.objects.get (pk = request.user.id)
	if usuarioLogueado.perfilActivo == 'Real':
		perfil=usuarioLogueado.perfilReal
	else:
		perfil=usuarioLogueado.perfilFalso
	numAmigos=perfil.amigos.count()

	diario_usuario = DiarioPersonal.objects.get (pk = diario_id)
	if request.method == 'POST':
		entradaPersonal = EntradaDiarioPersonal.objects.create (diarioPersonal = diario_usuario)
		form = EntradaDiarioPersonalForm (request.POST, instance = entradaPersonal)
		if form.is_valid ():
			form.save ()
			return redirect ('/usuario/')
	else:
		form = EntradaDiarioPersonalForm ()
	context = {'form': form,'perfil':perfil,'numAmigos':numAmigos}
	return render (request, 'diario/nueva_entrada.html', context)

# Diario pensamientos nueva entrada
def diarioPensamientosNuevaEntrada (request, diario_id):
	#usuario logueado
	usuarioLogueado = Usuario.objects.get (pk = request.user.id)
	if usuarioLogueado.perfilActivo == 'Real':
		perfil=usuarioLogueado.perfilReal
	else:
		perfil=usuarioLogueado.perfilFalso
	numAmigos=perfil.amigos.count()

	diario_usuario = DiarioPensamientos.objects.get (pk = diario_id)
	if request.method == 'POST':
		entradaPensamientos = EntradaDiarioPensamientos.objects.create (diarioPensamientos = diario_usuario)
		form = EntradaDiarioPensamientosForm (request.POST, instance = entradaPensamientos)
		if form.is_valid ():
			form.save ()
			return redirect ('/usuario/')
	else:
		form = EntradaDiarioPensamientosForm ()
	context = {'form': form,'perfil':perfil,'numAmigos':numAmigos}
	return render (request, 'diario/nueva_entrada.html', context)

# Detalles de una entrada de la agenda
def detallesEntradaAgenda (request, entrada_id):
	entrada = EntradaAgenda.objects.get (pk = entrada_id)
	#usuario logueado
	usuarioLogueado = Usuario.objects.get (pk = request.user.id)
	if usuarioLogueado.perfilActivo == 'Real':
		perfil=usuarioLogueado.perfilReal
	else:
		perfil=usuarioLogueado.perfilFalso
	numAmigos=perfil.amigos.count()
	context = {'entrada': entrada,'perfil':perfil,'numAmigos':numAmigos}
	return render (request, 'diario/detalles_entrada_agenda.html', context)

# Detalles de una entrada del diario personal
def detallesEntradaPersonal (request, entrada_id):
	entrada = EntradaDiarioPersonal.objects.get (pk = entrada_id)
	#usuario logueado
	usuarioLogueado = Usuario.objects.get (pk = request.user.id)
	if usuarioLogueado.perfilActivo == 'Real':
		perfil=usuarioLogueado.perfilReal
	else:
		perfil=usuarioLogueado.perfilFalso
	numAmigos=perfil.amigos.count()

	context = {'entrada': entrada,'perfil':perfil,'numAmigos':numAmigos}
	return render (request, 'diario/detalles_entrada_personal.html', context)

# Detalles de una entrada del diario de pensamientos
def detallesEntradaPensamientos (request, entrada_id):
	entrada = EntradaDiarioPensamientos.objects.get (pk = entrada_id)
	#usuario logueado
	usuarioLogueado = Usuario.objects.get (pk = request.user.id)
	if usuarioLogueado.perfilActivo == 'Real':
		perfil=usuarioLogueado.perfilReal
	else:
		perfil=usuarioLogueado.perfilFalso
	numAmigos=perfil.amigos.count()
	context = {'entrada': entrada,'perfil':perfil,'numAmigos':numAmigos}
	return render (request, 'diario/detalles_entrada_pensamientos.html', context)

# Editar una entrada de la agenda
def editarEntradaAgenda (request, entrada_id):
	#usuario logueado
	usuarioLogueado = Usuario.objects.get (pk = request.user.id)
	if usuarioLogueado.perfilActivo == 'Real':
		perfil=usuarioLogueado.perfilReal
	else:
		perfil=usuarioLogueado.perfilFalso
	numAmigos=perfil.amigos.count()

	entrada = EntradaAgenda.objects.get (pk = entrada_id)
	if request.method == 'POST':
		form = EntradaAgendaForm (request.POST, instance = entrada)
		if form.is_valid ():
			form.save ()
			return redirect ('/usuario/')
	else:
		form = EntradaAgendaForm (instance = entrada)
	context = {'form': form,'perfil':perfil,'numAmigos':numAmigos}
	return render (request, 'diario/editar_entrada.html', context)

# Editar una entrada del diario personal
def editarEntradaPersonal (request, entrada_id):
	#usuario logueado
	usuarioLogueado = Usuario.objects.get (pk = request.user.id)
	if usuarioLogueado.perfilActivo == 'Real':
		perfil=usuarioLogueado.perfilReal
	else:
		perfil=usuarioLogueado.perfilFalso
	numAmigos=perfil.amigos.count()

	entrada = EntradaDiarioPersonal.objects.get (pk = entrada_id)
	if request.method == 'POST':
		form = EntradaDiarioPersonalForm (request.POST, instance = entrada)
		if form.is_valid ():
			form.save ()
			return redirect ('/usuario/')
	else:
		form = EntradaDiarioPersonalForm (instance = entrada)
	context = {'form': form,'perfil':perfil,'numAmigos':numAmigos}
	return render (request, 'diario/editar_entrada.html', context)

# Editar una entrada del diario de pensamientos
def editarEntradaPensamientos (request, entrada_id):
	#usuario logueado
	usuarioLogueado = Usuario.objects.get (pk = request.user.id)
	if usuarioLogueado.perfilActivo == 'Real':
		perfil=usuarioLogueado.perfilReal
	else:
		perfil=usuarioLogueado.perfilFalso
	numAmigos=perfil.amigos.count()

	entrada = EntradaDiarioPensamientos.objects.get (pk = entrada_id)
	if request.method == 'POST':
		form = EntradaDiarioPensamientosForm (request.POST, instance = entrada)
		if form.is_valid ():
			form.save ()
			return redirect ('/usuario/')
	else:
		form = EntradaDiarioPensamientosForm (instance = entrada)
	context = {'form': form,'perfil':perfil,'numAmigos':numAmigos}
	return render (request, 'diario/editar_entrada.html', context)

# Eliminar una entrada de la agenda
def eliminarEntradaAgenda (request, entrada_id):
	entrada = EntradaAgenda.objects.get (pk = entrada_id)
	entrada.delete ()
	return render (request, 'diario/eliminar_entrada.html')

# Eliminar una entrada del diario pesonal
def eliminarEntradaPersonal (request, entrada_id):
	entrada = EntradaDiarioPersonal.objects.get (pk = entrada_id)
	entrada.delete ()
	return render (request, 'diario/eliminar_entrada.html')

# Eliminar una entrada del diario de pensamientos
def eliminarEntradaPensamientos (request, entrada_id):
	entrada = EntradaDiarioPensamientos.objects.get (pk = entrada_id)
	entrada.delete ()
	return render (request, 'diario/eliminar_entrada.html')
