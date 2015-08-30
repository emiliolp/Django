from django.conf.urls import patterns, include, url
from usuario import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  # Examples:
  # url(r'^$', 'ProyectoIW.views.home', name='home'),
  # url(r'^ProyectoIW/', include('ProyectoIW.foo.urls')),
  # Index para usuarios no registrados o no logueados
  url(r'^$', TemplateView.as_view(template_name='index.html'), name="index"),

  # Uncomment the admin/doc line below to enable admin documentation:
  # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

  # Uncomment the next line to enable the admin:
  url (r'^admin/', include(admin.site.urls)),
	url (r'usuario/',include('usuario.urls',namespace='usuario')),
	url (r'diario/', include ('diario.urls', namespace = 'diario')),
	url(r'^chat/', include('djangoChat.urls')),
	url(r'^fileTransfer/',include('fileTransfer.urls')),
)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
