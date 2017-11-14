from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.welcome, name='welcome'),
	url(r'^contatti/$', views.contatti, name='contatti'),
	url(r'^signup/$', views.signup, name='iscrizione'),
]
