from django.shortcuts import render, HttpResponse, get_object_or_404
from django.template import loader
from .models import Recensione
from django.http import Http404, HttpResponseRedirect
from .forms import ResearchForm, ReviewForm
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from LD_Proj.settings import URL_FORM, LOGIN_URL 
from portal.utility import suggestFilm, anonymous, isOfficial
from recensioni.forms import CommentForm

url_index = 'recensioni/index.html'
url_detail = 'recensioni/detail.html'
url_insert = URL_FORM
url_ricerca = URL_FORM

# View generica per renderizzare una lista di recensioni
# Questa funzione è troppo poco generica, non serve a niente, tbh
def list_render (request, lista, context):
	try:
		context.update({'recensioni':lista, 'request':request})
	except:
		context = {'recensioni':lista, 'request':request}
	return render(request, url_index, context)

"""class IndexView(generic.ListView):
	template_name = url_index
	context_object_name = 'recensioni'
	def get_queryset(self):
		return Recensione.objects.all()"""

# View dell'elenco completo delle recensioni
def elenco (request):
	lista = Recensione.objects.order_by('-pub_date')
	context = {'titolo':'Elenco completo'}
	return list_render (request, lista, context) 


# View dettagli della singola recensione
def detail (request, rec_id):
    recensione = get_object_or_404(Recensione, pk=rec_id)
    titolo = "Recensione "+rec_id
    context = {'recensione':recensione, 'titolo':titolo}
    return render(request, url_detail, context)

# View della pagina di ricerca
def ricerca (request):
	# Profilazione della ricerca, se l'utente è loggato
	user = request.user
	suggestList = suggestFilm(user)
	if request.method == 'POST': #invio
		form = ResearchForm(request.POST)
		context = {'titolo':'Risultati ricerca', 'suggerimenti':1}
		if form.is_valid():
			title = form.cleaned_data['titolo']
			result = Recensione.objects.filter(titolo__contains=title)
			genre = form.cleaned_data['genere']
			if genre:
				result = result.filter(genere__startswith=genre)
			nComments = form.cleaned_data['ncomm']
			if nComments:
				tmp_list = []
				for recensione in result.iterator():
					if (recensione.commento_set.count() >= nComments):
						tmp_list.append(recensione) 
				result = tmp_list
			for film in result:
				if film in suggestList:
						suggestList.remove(film)
			# Passo i primi film della lista suggerimenti..
			context['lista_sugg'] = suggestList[:5]
			return list_render (request, result, context)
		else:
			messages.add_message(request, messages.INFO, 
						'Errore: Hai inserito un tipo di dato non valido.')
			return HttpResponseRedirect(reverse('recensioni:ricerca'))
	else: # visualizzazione
		form = ResearchForm()
		context = {'titolo':'Ricerca', 'form':form}
		return render(request, url_ricerca, context)
	
""" 
Questa pagina presenta le recensioni più in voga, che per semplicità
ho deciso essere le recensioni più votate.
Il numero dei voti è poi moltiplicato per un coefficente che dipende dal rank
globale della recensione attualmente.
Nelle prossime versioni sarà introdotto una funzione che sfrutta la profilazione
degli utenti ottenuta da portal.
L'algoritmo di ordinamento altro non è che la funzione sorted() di python.
"""
@method_decorator(login_required(), name='dispatch')
class top100view (generic.ListView):
	template_name = url_index
	#context_object_name = 'recensioni'
	
	def get_queryset(self):
		list = {}
		for recensione in Recensione.objects.all():
			if (recensione.num_voti() >= 1):
				list[recensione]=recensione.num_voti()*recensione.getRank()
		return sorted(list, key=list.get, reverse=True)[:100]
	
	def get_context_data(self, **kwargs):
		context = super(top100view, self).get_context_data(**kwargs)
		context['recensioni'] = self.get_queryset
		context['voti_on'] = 1
		context['titolo'] = 'Top100 Recensioni'
		return context
	

"""
View per l'inserimento di nuove recensioni.
Necessità di essere loggati e avere permesso di postare.
Permesso presente di default, che però può essere rimosso dagli admin.
In caso di mancanza del permesso si viene reindirizzati ad un 403.
"""
@login_required
@permission_required('recensioni.add_recensione', raise_exception=True)
def insert_review (request):
	if request.method == 'GET':	
		form = ReviewForm()
		contest = {'form':form, 'titolo':'Nuova recensione'}
		return render(request, url_insert, contest)
	else:
		form = ReviewForm(request.POST)
		recensione = form.save(commit=False)
		recensione.rank = 50
		if (recensione.autore != anonymous()) :
			recensione.autore = request.user
			if isOfficial(request.user):
				recensione.rank = 80
		if form.is_valid():
			recensione.save()
			form.save_m2m()
			messages.add_message(request, messages.INFO, 
						'Ottimo, la tua recensione è stata inserita!')
			return HttpResponseRedirect(reverse('recensioni:elenco'))
		else:
			messages.add_message(request, messages.INFO, 
						'Errore: Hai inserito un tipo di dato non valido.')
			return HttpResponseRedirect(reverse('recensioni:nuovarec'))

@login_required
@permission_required('recensioni.add_commento', raise_exception=True)
def insert_comment (request, rec_id):
	recensione = get_object_or_404(Recensione, pk=rec_id)
	if request.method == 'GET':
		form = CommentForm()
		contest = {'form':form, 'titolo':'Nuovo commento'}
		return render(request, url_insert, contest)
	else :
		form = CommentForm(request.POST)
		commento = form.save(commit=False)
		commento.recensione = recensione
		commento.autore = request.user
		commento.save()
		recensione.__rankUpdate__() # forzo aggiornamento del rank
		return render(request, url_detail, {'recensione':recensione})
