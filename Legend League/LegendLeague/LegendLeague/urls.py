from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from principal import views
from news import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$','principal.views.inicio'),
	url(r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    #jornada
    url(r'^principal/calendario/proxima_jornada/$','principal.views.ProximaJornada'),
    url(r'^principal/calendario/$','principal.views.JornadaList',name='jornada_list'),
    url(r'^principal/calendario/jornada(?P<jornada_id>\d+)$','principal.views.JornadaDetail',name='jornada_detail'),
    url(r'^principal/calendario/nueva_jornada/$','principal.views.NuevaJornada'),
    url(r'^principal/calendario/jornada(?P<jornada_id>\d+)/editar_jornada/$','principal.views.EditJornada'),
    url(r'^principal/calendario/jornada(?P<jornada_id>\d+)/eliminar_jornada/$','principal.views.JornadaDelete'),

    #partido
    url(r'^principal/calendario/jornada(?P<jornada_id>\d+)/nuevo_partido/$','principal.views.NuevoPartido'),
    url(r'^principal/calendario/jornada(?P<jornada_id>\d+)/(?P<partido_id>\d+)$','principal.views.PartidoDetail',name='partido_detail'),
    url(r'^principal/calendario/jornada(?P<jornada_id>\d+)/(?P<partido_id>\d+)/editar_partido/$','principal.views.EditPartido'),
    url(r'^principal/calendario/jornada(?P<jornada_id>\d+)/(?P<partido_id>\d+)/eliminar_partido/$','principal.views.PartidoDelete'),

    #Estadisticas
    url(r'^principal/clasificacion/$','principal.views.Clasificacion',name='clasificacion'),
    url(r'^principal/goleadores/$','principal.views.Goleadores'),
    url(r'^principal/sanciones/$','principal.views.Sanciones'),

    #equipos
    url(r'^principal/equipos/$','principal.views.EquipoList',name='equipos'),
    url(r'^principal/equipos/(?P<equipo_id>\d+)$','principal.views.EquipoDetail',name='equipo_detail'),
    url(r'^principal/equipos/nuevo_equipo/$','principal.views.NuevoEquipo',name='new_team'),
    url(r'^principal/equipos/(?P<equipo_id>\d+)/edit/$','principal.views.edit_team'),
    url(r'^principal/equipos/(?P<equipo_id>\d+)/eliminar_equipo/$','principal.views.EquipoDelete'),

    #jugadores
    url(r'^principal/equipos/(?P<equipo_id>\d+)/nuevo_jugador/$','principal.views.NuevoJugador'),
    url(r'^principal/equipos/(?P<equipo_id>\d+)/(?P<jugador_id>\d+)/editar_jugador/$','principal.views.EditarJugador'),
    url(r'^principal/equipos/(?P<equipo_id>\d+)/(?P<jugador_id>\d+)/$','principal.views.JugadorDetail'),
    url(r'^principal/equipos/(?P<equipo_id>\d+)/(?P<jugador_id>\d+)/eliminar_jugador/$','principal.views.JugadorDelete'),

    #participaciones de jugadores
    url(r'^principal/equipos/(?P<equipo_id>\d+)/(?P<jugador_id>\d+)/participa(?P<participa_id>\d+)/$','principal.views.ParticipaDetail'),
    url(r'^principal/equipos/(?P<equipo_id>\d+)/(?P<jugador_id>\d+)/nueva_participacion/$','principal.views.ParticipaNuevo'),
    url(r'^principal/equipos/(?P<equipo_id>\d+)/(?P<jugador_id>\d+)/participa(?P<participa_id>\d+)/editar_participacion/$','principal.views.ParticipaEditar'),
    url(r'^principal/equipos/(?P<equipo_id>\d+)/(?P<jugador_id>\d+)/participa(?P<participa_id>\d+)/eliminar_participacion/$','principal.views.ParticipaDelete'),

    #usuarios
    url(r'^users/login$','principal.views.userLogin',name='login'),
    url(r'^principal/users/logout/$','principal.views.Logout',name='logout'),
    url(r'^principal/users/nuevo_usuario/$','principal.views.NuevoUsuario',name='new_user'),
    url(r'^users/(?P<user_id>\d+)/$','principal.views.userDetail'),
    url(r'^users/(?P<user_id>\d+)/edit_user/$','principal.views.editarUsuario'),
    url(r'^users/(?P<user_id>\d+)/eliminar_user/$','principal.views.eliminarUsuario'),
    
    #arbitros
    url(r'^principal/arbitros/$','principal.views.ArbitroList'),
    url(r'^principal/arbitros/(?P<arbitro_id>\d+)$','principal.views.ArbitroDetail'),
    url(r'^principal/arbitros/nuevo_arbitro/$','principal.views.NuevoArbitro'),
    url(r'^principal/arbitros/(?P<arbitro_id>\d+)/edit/$','principal.views.EditarArbitro'),
    url(r'^principal/arbitros/(?P<arbitro_id>\d+)/eliminar_arbitro/$','principal.views.ArbitroDelete'),

    #noticias
    url(r'^noticias/$','news.views.NoticiaList'),
    url(r'^noticias/(?P<noticia_id>\d+)/$','news.views.NoticiaDetail'),
    url(r'^noticias/(?P<noticia_id>\d+)/editar_noticia/$','news.views.editarNoticia'),
    url(r'^noticias/nueva_noticia/$','news.views.nuevaNoticia'),
    url(r'^noticias/(?P<noticia_id>\d+)/eliminar_noticia/$','news.views.eliminarNoticia')
    
) + static(settings.STATIC_URL,document_root= settings.STATIC_ROOT) + static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)
