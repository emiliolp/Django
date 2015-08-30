# Create your views here.
from django.shortcuts import render,redirect
from django.conf import settings
from principal.models import Equipo,Jugador,Arbitro,Jornada,Partido,Participa
from news.models import New
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import TemplateView
#from .forms import TeamForm
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.core.context_processors import csrf
from django.forms.models import modelform_factory,modelformset_factory
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from principal.forms import UserCreationForm,MyUserForm,TeamForm,JornadaForm,PartidoForm,ArbitroForm,JugadorForm,ParticipaForm
from django.db.models import Avg,Max,Min,Count
from django.contrib.auth.models import User



def inicio(request):
	list=Equipo.objects.all()
	noticias=New.objects.all().order_by('-id')
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	context = {'equipoList':list,'newList':noticias,'partidoList':partidos}
	return render(request,'index.html', context)

def userLogin(request):
	list=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	if request.method == 'POST':
        	form = AuthenticationForm(request.POST,request.FILES)
       		if form.is_valid:
            		user = request.POST['username']
            		passwd = request.POST['password']
            		access = authenticate(username=user, password=passwd)
            		if access is not None:
                		if access.is_active:
                    			login(request, access)
                    			return redirect('/')
                		else:
                    			return render(request, 'inactive.html')
            		else:
                		return render(request, 'nouser.html')
    	else:
        	form = AuthenticationForm()
	context = {'form': form,'equipoList':list,'partidoList':partidos}
	return render(request,'login.html', context)

@login_required(login_url='/users/login')
def userDetail(request,user_id):
	list=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	user=User.objects.get(pk=user_id)
	context={'user':user,'equipoList':list,'partidoList':partidos}
	return render(request,'user.html',context)

@login_required(login_url='/users/login')
def editarUsuario(request,user_id):
	list=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	usuario=get_object_or_404(User,pk=user_id)
	if request.method=='POST':
		form=MyUserForm(request.POST,request.FILES,instance=usuario)
		if form.is_valid():
			form.save()
			return redirect('/')
	else:
		form=MyUserForm(instance=usuario)

	context={'form':form,'equipoList':list,'partidoList':partidos}
	return render(request,'newuser.html',context)

@login_required(login_url='/users/login')
def eliminarUsuario(request, user_id):
    usuario = get_object_or_404(User, pk = user_id)
    usuario.delete()
    return redirect('/')

def JornadaList (request):
	equipos=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	list=Jornada.objects.all()
	context={'jornadaList':list,'equipoList':equipos,'partidoList':partidos}
	return render (request,'jornadas.html',context)

@login_required(login_url='/users/login')
def NuevaJornada(request):
	list=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	if request.method=='POST':
		form=JornadaForm(request.POST,request.FILES)
		if form.is_valid():
			form.save()
			return redirect('/principal/calendario')
	else:
		form=JornadaForm()

	context={'form':form,'equipoList':list,'partidoList':partidos}
	return render(request,'jornadaform.html',context)

def JornadaDetail(request,jornada_id):
	jornada=jornada_id
	equipos=Equipo.objects.all()
	list=Partido.objects.filter(jornada=jornada_id)
	context={'partidoList':list,'equipoList':equipos,'jornada':jornada}
	return render(request,'partidos.html',context)

@login_required(login_url='/users/login')
def EditJornada(request,jornada_id):
	list=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	jornada=get_object_or_404(Jornada,pk=jornada_id)
	if request.method=='POST':
		form=JornadaForm(request.POST,request.FILES,instance=jornada)
		if form.is_valid():
			form.save()
			return redirect('/principal/calendario')
	else:
		form=JornadaForm(instance=jornada)

	context={'form':form,'equipoList':list,'partidoList':partidos}
	return render(request,'jornadaform.html',context)

@login_required(login_url='/users/login')
def JornadaDelete(request, jornada_id):
    jornada = get_object_or_404(Jornada, pk = jornada_id)
    jornada.delete()
    return redirect('/principal/calendario')

def ProximaJornada(request):
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	equipos=Equipo.objects.all()
	list=Partido.objects.filter(jornada=jornada_id)
	context={'partidoList':list,'equipoList':equipos,'jornada':jornada_id}
	return render(request,'proxima_jornada.html',context)

@login_required(login_url='/users/login')
def NuevoPartido(request,jornada_id):
	list=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	if request.method=='POST':
		form=PartidoForm(request.POST,request.FILES)
		if form.is_valid():
			form.save()
			return redirect('/principal/calendario/jornada%s'%jornada_id)
	else:
		form=PartidoForm()

	context={'form':form,'partidoList':partidos,'equipoList':list}
	return render(request,'partidoform.html',context)

def PartidoDetail(request,jornada_id,partido_id):
	list=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	goles=Participa.objects.filter(partido=partido_id,goles__gt=0)
	amarillas=Participa.objects.filter(partido=partido_id,amarilla__gt=0)
	rojas=Participa.objects.filter(partido=partido_id,roja__gt=0)
	partido=Partido.objects.get(pk=partido_id)
	estadio=Partido.objects.get(id=1).nombre_equipo_casa.nombre_estadio
	equipos=Equipo.objects.all()
	context={'golesList':goles,'amarillasList':amarillas,'rojasList':rojas,'partido':partido,'estadio':estadio,'equipoList':equipos,'partidoList':partidos,'equipoList':list}
	return render(request,'partido.html',context)

@login_required(login_url='/users/login')
def EditPartido(request,jornada_id,partido_id):
	list=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	partido=get_object_or_404(Partido,pk=partido_id)
	if request.method=='POST':
		form=PartidoForm(request.POST,request.FILES,instance=partido)
		if form.is_valid():
			form.save()
			return redirect("/principal/calendario/jornada%s"%jornada_id)
	else:
		form=PartidoForm(instance=partido)

	context={'form':form,'partidoList':partidos,'equipoList':list}
	return render(request,'partidoform.html',context)

@login_required(login_url='/users/login')
def PartidoDelete(request, jornada_id,partido_id):
    partido = get_object_or_404(Partido, pk = partido_id)
    partido.delete()
    return redirect('/principal/calendario/jornada%s'%jornada_id)

@login_required(login_url='/users/login')
def NuevoJugador(request,equipo_id):
	list=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	if request.method=='POST':
		form=JugadorForm(request.POST,request.FILES)
		if form.is_valid():
			form.save()
			return redirect("/principal/equipos/%s"%equipo_id)
	else:
		form=JugadorForm()

	context={'form':form,'partidoList':partidos,'equipoList':list}
	return render(request,'jugadorform.html',context)

@login_required(login_url='/users/login')
def EditarJugador(request,equipo_id,jugador_id):
	list=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	jugador=get_object_or_404(Jugador,pk=jugador_id)
	if request.method=='POST':
		form=JugadorForm(request.POST,request.FILES,instance=jugador)
		if form.is_valid():
			form.save()
			return redirect("/principal/equipos/%s"%equipo_id)
	else:
		form=JugadorForm(instance=jugador)

	context={'form':form,'partidoList':partidos,'equipoList':list}
	return render(request,'jugadorform.html',context)

@login_required(login_url='/users/login')
def JugadorDelete(request, equipo_id,jugador_id):
    jugador = get_object_or_404(Jugador, pk = jugador_id)
    jugador.delete()
    return redirect('/principal/equipos/%s'%equipo_id)


def Clasificacion(request):
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	equipos=Equipo.objects.all()
	list=Equipo.objects.all().order_by('posicion')
	p=Equipo.objects.filter(nombre_equipo='Inter de Mitente').values('id')
	partidos_jugados=Partido.objects.filter(nombre_equipo_fuera=p).count() | Partido.objects.filter(nombre_equipo_casa=p).count()
	#partidos_jugados=Equipo.objects.values('partidos_ganados')+Equipo.objects.values('partidos_empatados')
	context={'clasificacion':list,'equipoList':equipos,'partidoList':partidos}
	return render(request,'clasificacion.html',context)

def Goleadores(request):
	list=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	goleadores=Jugador.objects.filter(goles__gt=0).order_by('-goles')
	context={'goleadoresList':goleadores,'partidoList':partidos,'equipoList':list}
	return render(request,'goleadores.html',context)

def Sanciones(request):
	list=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	sanciones=Jugador.objects.filter(tarjetas_amarillas__gt=0).order_by('-tarjetas_rojas','-tarjetas_amarillas') | Jugador.objects.filter(tarjetas_rojas__gt=0).order_by('-tarjetas_rojas','-tarjetas_amarillas')
	context={'sancionesList':sanciones,'partidoList':partidos,'equipoList':list}
	return render(request,'sanciones.html',context)

def EquipoList(request):
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	list=Equipo.objects.all()
	context={'equipoList':list,'partidoList':partidos}
	return render(request,'equipos.html',context)

def EquipoDetail(request,equipo_id):
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	equipos=Equipo.objects.all()
	equipo=Equipo.objects.get(pk=equipo_id)
	plantilla=Jugador.objects.filter(equipo=equipo_id)
	context={'equipo':equipo,'equipoList':equipos,'jugadorList':plantilla,'partidoList':partidos}
	return render(request,'equipo.html',context)

@login_required(login_url='/users/login')
def EquipoDelete(request, equipo_id):
    equipo = get_object_or_404(Equipo, pk = equipo_id)
    equipo.delete()
    return redirect('/principal/equipos')

def JugadorDetail(request,equipo_id,jugador_id):
	list=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	jugador=Jugador.objects.get(pk=jugador_id)
	equipo=Equipo.objects.get(pk=equipo_id)
	participaciones=Participa.objects.filter(jugador=jugador_id)
	context={'jugador':jugador,'equipo':equipo,'participasList':participaciones,'equipoList':list,'partidoList':partidos}
	return render(request,'jugador.html',context)

def ParticipaDetail(request,equipo_id,jugador_id,participa_id):
	list=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	participa=Participa.objects.get(pk=participa_id)
	equipo=equipo_id
	jugador=jugador_id
	context={'participa':participa,'equipo':equipo,'jugador':jugador,'equipoList':list,'partidoList':partidos}
	return render(request,'participa.html',context)

@login_required(login_url='/users/login')
def ParticipaNuevo(request,equipo_id,jugador_id):
	list=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	if request.method=='POST':
		form=ParticipaForm(request.POST,request.FILES)
		if form.is_valid():
			form.save()
			return redirect('/principal/equipos/%s/%s'%(equipo_id,jugador_id))
	else:
		form=ParticipaForm()

	context={'form':form,'equipoList':list,'partidoList':partidos}
	return render(request,'participaform.html',context)

@login_required(login_url='/users/login')
def ParticipaEditar(request,equipo_id,jugador_id,participa_id):
	list=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	participa=get_object_or_404(Participa,pk=participa_id)
	if request.method=='POST':
		form=ParticipaForm(request.POST,request.FILES,instance=participa)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/principal/equipos/%s/%s"%(equipo_id,jugador_id))
	else:
		form=ParticipaForm(instance=participa)

	context={'form':form,'equipoList':list,'partidoList':partidos}
	return render(request,'participaform.html',context)

@login_required(login_url='/users/login')
def ParticipaDelete(request,equipo_id,jugador_id,participa_id):
	participa = get_object_or_404(participa, pk = participa_id)
    	participa.delete()
    	return redirect('/principal/equipos/%s/%s'%(equipo_id,jugador_id))

def ArbitroList(request):
	equipos=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	list=Arbitro.objects.all()
	context={'arbitroList':list,'equipoList':equipos,'partidoList':partidos}
	return render(request,'arbitros.html',context)

def ArbitroDetail(request,arbitro_id):
	list=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	arbitro=Arbitro.objects.get(pk=arbitro_id)
	context={'arbitro':arbitro,'equipoList':list,'partidoList':partidos}
	return render(request,'arbitro.html',context)

@login_required(login_url='/users/login')
def NuevoArbitro(request):
	list=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	if request.method=='POST':
		form=ArbitroForm(request.POST,request.FILES)
		if form.is_valid():
			form.save()
			return redirect('/principal/arbitros/')
	else:
		form=ArbitroForm()

	context={'form':form,'equipoList':list,'partidoList':partidos}
	return render(request,'arbitroform.html',context)

@login_required(login_url='/users/login')
def EditarArbitro(request,arbitro_id):
	list=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	arbitro=get_object_or_404(Arbitro,pk=arbitro_id)
	if request.method=='POST':
		form=ArbitroForm(request.POST,request.FILES,instance=arbitro)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/principal/arbitros/")
	else:
		form=ArbitroForm(instance=arbitro)

	context={'form':form,'equipoList':list,'partidoList':partidos}
	return render(request,'arbitroform.html',context)

@login_required(login_url='/users/login')
def ArbitroDelete(request, arbitro_id):
    arbitro = get_object_or_404(Arbitro, pk = arbitro_id)
    arbitro.delete()
    return redirect('/principal/arbitros')

#def Sanciones(request):

@login_required(login_url='/users/login')
def Logout(request):
   	logout(request)
	return redirect('/')

def NuevoUsuario(request):
	list=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	if request.method=='POST':
		form=MyUserForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	else:
		form=MyUserForm()
	context={'form':form,'equipoList':list,'partidoList':partidos}
	return render(request,'newuser.html',context)

@login_required(login_url='/users/login')
def NuevoEquipo(request):
	list=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	if request.method=='POST':
		form=TeamForm(request.POST,request.FILES)
		if form.is_valid():
			form.save()
			return redirect('/principal/equipos')
	else:
		form=TeamForm()

	context={'form':form,'equipoList':list,'partidoList':partidos}
	return render(request,'teamform.html',context)

@login_required(login_url='/users/login')
def edit_team(request,equipo_id):
	list=Equipo.objects.all()
	jornada_id=Jornada.objects.filter(terminada=False).annotate(Max('numero'))
	partidos=Partido.objects.filter(jornada=jornada_id)
	team=get_object_or_404(Equipo,pk=equipo_id)
	if request.method=='POST':
		form=TeamForm(request.POST,request.FILES,instance=team)
		if form.is_valid():
			form.save()
			return redirect('/principal/equipos/')
	else:
		form=TeamForm(instance=team)

	context={'form':form,'equipoList':list,'partidoList':partidos}
	return render(request,'teamform.html',context)





