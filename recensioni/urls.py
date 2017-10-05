from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.elenco, name='elenco'),
	url(r'^scrivi/$', views.insert_review, name='nuovarec'),
	url(r'^(?P<rec_id>[0-9]+)/commento/$', views.insert_comment, name='comment'),
	#url(r'^(?P<rec_id>[0-9]+)/$', views.detail, name='dettaglio'),
	url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='dettaglio'),
	url(r'^ricerca/$', views.ricerca, name='ricerca'),
	url(r'^top/$', views.top100view.as_view(), name='top100'), 
]
