from django.conf.urls import patterns, url

from fileTransfer import views

urlpatterns = patterns('',
    
    url(r'^listFiles/$', views.listFiles, name='listFiles'),
   
)