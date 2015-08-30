# Create your views here.
from django.shortcuts import render,redirect
from django.conf import settings
from .models import New
from django.shortcuts import render_to_response,get_object_or_404
from news.forms import NoticiaForm
from django.contrib.auth.decorators import login_required
from principal.models import Equipo,Jugador,Arbitro,Jornada,Partido,Participa
from django.db.models import Avg,Max,Min,Count

def NoticiaList (request):
	equipos=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	list=New.objects.all()
	context={'newList':list,'equipoList':equipos,'partidoList':partidos}
	return render (request,'noticias.html',context)

def NoticiaDetail(request,noticia_id):
	list=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	noticia=New.objects.get(pk=noticia_id)
	context={'noticia':noticia,'equipoList':list,'partidoList':partidos}
	return render(request,'noticia.html',context)

@login_required(login_url='/users/login')
def nuevaNoticia(request):
	list=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	if request.method=='POST':
		form=NoticiaForm(request.POST,request.FILES)
		if form.is_valid():
			form.save()
			return redirect('/noticias')
	else:
		form=NoticiaForm()

	context={'form':form,'equipoList':list,'partidoList':partidos}
	return render(request,'noticiaform.html',context)

@login_required(login_url='/users/login')
def editarNoticia(request,noticia_id):
	list=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	noticia=get_object_or_404(New,pk=noticia_id)
	if request.method=='POST':
		form=NoticiaForm(request.POST,request.FILES,instance=noticia)
		if form.is_valid():
			form.save()
			return redirect('/noticias')
	else:
		form=NoticiaForm(instance=noticia)

	context={'form':form,'equipoList':list,'partidoList':partidos}
	return render(request,'noticiaform.html',context)

@login_required(login_url='/users/login')
def eliminarNoticia(request,noticia_id):
	noticia = get_object_or_404(New, pk = noticia_id)
    	noticia.delete()
    	return redirect('/noticias')

