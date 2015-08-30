from django.conf.urls import patterns, include, url
from diario import views

urlpatterns=patterns('',
	# Ver agenda
	url (r'entradas-agenda-(?P<usuario_id>\d+)$', views.verAgenda, name = 'verAgenda'),
	# Ver diario personal
	url (r'entradas-personal-(?P<usuario_id>\d+)$', views.verDiarioPersonal, name = 'verDiarioPersonal'),
	# Ver diario pensamientos
	url (r'entradas-pensamientos-(?P<usuario_id>\d+)$', views.verDiarioPensamientos, name = 'verDiarioPensamientos'),
	# Agenda nueva entrada
	url (r'agenda-nueva-entrada-(?P<agenda_id>\d+)$', views.agendaNuevaEntrada, name = 'agendaNuevaEntrada'),
	# Diario personal nueva entrada
	url (r'personal-nueva-entrada-(?P<diario_id>\d+)$', views.diarioPersonalNuevaEntrada, name = 'diarioPersonalNuevaEntrada'),
	# Diario pensamientos nueva entrada
	url (r'pensamientos-nueva-entrada-(?P<diario_id>\d+)$', views.diarioPensamientosNuevaEntrada, name = 'diarioPensamientosNuevaEntrada'),
	# Detalles de una entrada de la agenda
	url (r'detalles-entrada-agenda-(?P<entrada_id>\d+)$', views.detallesEntradaAgenda, name = 'detallesEntradaAgenda'),
	# Detalles de una entrada del diario personal
	url (r'detalles-entrada-personal-(?P<entrada_id>\d+)$', views.detallesEntradaPersonal, name = 'detallesEntradaPersonal'),
	# Detalles de una entrada del diario de pensamientos
	url (r'detalles-entrada-pensamientos-(?P<entrada_id>\d+)$', views.detallesEntradaPensamientos, name = 'detallesEntradaPensamientos'),
	# Editar una entrada de la agenda
	url (r'editar-entrada-agenda-(?P<entrada_id>\d+)$', views.editarEntradaAgenda, name = 'editarEntradaAgenda'),
	# Editar una entrada del diario personal
	url (r'editar-entrada-personal-(?P<entrada_id>\d+)$', views.editarEntradaPersonal, name = 'editarEntradaPesonal'),
	# Editar una entrada del diario de pensamientos
	url (r'editar-entrada-pensamientos-(?P<entrada_id>\d+)$', views.editarEntradaPensamientos, name = 'editarEntradaPensamientos'),
	# Eliminar una entrada de la agenda
	url (r'eliminar-entrada-agenda-(?P<entrada_id>\d+)$', views.eliminarEntradaAgenda, name = 'eliminarEntradaAgenda'),
	# Eliminar una entrada del diario personal
	url (r'eliminar-entrada-personal-(?P<entrada_id>\d+)$', views.eliminarEntradaPersonal, name = 'eliminarEntradaPersonal'),
	# Eliminar una entrada del diario de pensamientos
	url (r'eliminar-entrada-pensamientos-(?P<entrada_id>\d+)$', views.eliminarEntradaPensamientos, name = 'eliminarEntradaPensamientos'),
)
