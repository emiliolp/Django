# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # Paginator
from django.shortcuts import render, redirect, get_object_or_404 # Redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from usuario.models import Usuario,PerfilUsuario
from diario.forms import EntradaAgendaForm, EntradaDiarioPersonalForm, EntradaDiarioPensamientosForm

from .models import *
from .forms import *

def listFiles(request):
	#usuario logueado
	usuarioLogueado = Usuario.objects.get (pk = request.user.id)
	if usuarioLogueado.perfilActivo == 'Real':
		perfil=usuarioLogueado.perfilReal
	else:
		perfil=usuarioLogueado.perfilFalso
	numAmigos=perfil.amigos.count()
	# Handle file upload
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			newdoc = files(docfile = request.FILES['docfile'])
			newdoc.save()
			
			return redirect('/fileTransfer/listFiles/')
			
	else:
		form = DocumentForm() 
	documents = files.objects.all()
	context={'documents':documents, 'form':form,'perfil':perfil,'numAmigos':numAmigos}
	return render(request, 'list_files.html', context)