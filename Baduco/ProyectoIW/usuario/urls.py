from django.conf.urls import patterns, include, url
from usuario import views

urlpatterns=patterns('',
	# Index para usuarios logueados
	url (r'^$', views.indexUsuario, name = 'indexUsuario'), #si
	# Registrar nuevo usuario
	url (r'nuevo-usuario$', views.nuevoUsuario, name = 'usuarioNuevo'), #no
	# Crear perfil real usuario
	url (r'crear-perfil-real$', views.crearPerfilReal, name = 'crearPerfilReal'), #no
	# Crear perfil falso usuario
	url (r'crear-perfil-falso$', views.crearPerfilFalso, name = 'crearPerfilFalso'), #no
	# Listar perfiles
	url (r'buscar-perfil$',views.buscar,name='buscarPerfiles'), #si
	# Detalles perfil
	url (r'usuario-(?P<usuario_id>\d+)/(?P<latitud_value>.\d+\.\d+)/(?P<longitud_value>.\d+\.\d+)/$', views.detallesPerfil, name = 'detallesPerfil'),
	# Ver perfil
	url (r'ver-perfil-(?P<perfil_id>\d+)$', views.verPerfil,name = 'verPerfil'),
	# Editar perfil
	url (r'editar-perfil-(?P<perfil_id>\d+)$', views.editarPerfil, name = 'editarPerfil'),
	# Gente cerca
	url (r'gente_cerca-(?P<usuario_id>\d+)/(?P<latitud_value>.\d+\.\d+)/(?P<longitud_value>.\d+\.\d+)/$',views.mostrarGenteCerca,name='genteCerca'),
	# Cambiar perfil
	url (r'cambiar-perfil$', views.cambiarPerfil, name = 'cambiarPerfil'),
	# Buscar personas
	url (r'buscar-usuario$', views.buscarUsuario, name = 'buscarUsuario'),
	# Enviar peticion de amistad
	url (r'enviar-peticion-amistad-(?P<perfil_id>\d+)$', views.enviarPeticionAmistad, name = 'enviarPeticionAmistad'),
	# Dejar de seguir
	url (r'dejar-seguir-(?P<perfil_id>\d+)$', views.dejarSeguir, name = 'dejarSeguir'),
	# Ver peticiones de amistad
	url (r'ver-peticiones-amistad-(?P<usuario_id>\d+)$', views.verPeticionesAmistad, name = 'verPeticionesAmistad'),
	# Detalles de una peticion de amistad
	url (r'detalles-peticion-amistad-(?P<peticion_id>\d+)$', views.detallesPeticionAmistad, name = 'detallesPeticionAmistad'),
	# Aceptar peticion de amistad
	url (r'aceptar-peticion-amistad-(?P<peticion_id>\d+)$', views.aceptarPeticionAmistad, name = 'aceptarPeticionAmistad'),
	# Rechazar peticion de amistad
	url (r'rechazar-peticion-amistad-(?P<peticion_id>\d+)$', views.rechazarPeticionAmistad, name = 'rechazarPeticionAmistad'),
	# Ver amigos
	url (r'ver-amigos-(?P<perfil_id>\d+)$', views.verAmigos, name = 'verAmigos'),
	# Hacer comentario a un perfil
	url (r'nuevo-comentario-(?P<perfil_id>\d+)$', views.nuevoComentario, name = 'nuevoComentario'),
	# Ver detalles de un comentario
	url (r'detalles-comentario-(?P<comentario_id>\d+)$', views.detallesComentario, name = 'detallesComentario'),
	# Hacer comentario a un comentario
	url (r'hacer-comentario-(?P<comentario_id>\d+)$', views.hacerComentario, name = 'hacerComentario'),
	# Votar perfil
	url (r'votar-perfil-(?P<perfil_id>\d+)$', views.votarPerfil, name = 'votarPerfil'),
	# Login
	url (r'login$', views.usuarioLogin, name = 'usuarioLogin'),
	# Logout
	url (r'logout$', views.usuarioLogout, name = 'usuarioLogout'),
)
