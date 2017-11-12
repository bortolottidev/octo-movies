from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^scrivi/$', views.insert_review, name='nuovarec'),
	url(r'^ricerca/$', views.ricerca, name='ricerca'),
	url(r'^top/$', views.top100view.as_view(), name='top100'), 
	url(r'^(?P<rec_id>[0-9]+)/commento/$', views.insert_comment, name='comment'),
	#url(r'^(?P<rec_id>[0-9]+)/$', views.detail, name='dettaglio'),
	url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='dettaglio'),
	# include anche la stringa vuota
	url(r'^(?P<filterStr>([0-9]*[a-zA-Z]+[0-9]*)*)[/]{0,1}$', views.elenco, name='elenco'),
]
