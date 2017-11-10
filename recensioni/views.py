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

# Funzione generica per renderizzare una lista di recensioni 
# La lista viene inserita nel context con il nome 'recensioni'
def list_render (request, lista, context):
	try:
		context.update({'recensioni':lista, 'request':request})
	except:
		context = {'recensioni':lista, 'request':request}
	return render(request, url_index, context)

<<<<<<< HEAD
# View dell'elenco delle recensioni
def elenco (request, filterStr):
	if filterStr == '':
		lista = Recensione.objects.order_by('-pub_date')
	elif filterStr.startswith("BEST"):
		year = filterStr[-4:]
		lista = Recensione.objects.filter(pub_date__year=year)

		## OK, ho quelle di quell'anno.. ma come ottenere il bestof? ##

	elif filterStr == 'Commedia' or filterStr == 'Azione':
		lista = Recensione.objects.filter(genere=filterStr)
	else:
		lista = Recensione.objects.filter(titolo__startswith=filterStr)
=======
# View dell'elenco completo delle recensioni
def elenco (request):
	lista = Recensione.__allRec__()
>>>>>>> master
	context = {'titolo':'Elenco completo'}
	return list_render (request, lista, context) 


## View dettagli della singola recensione
#def detail (request, rec_id):
    #recensione = get_object_or_404(Recensione, pk=rec_id)
    #titolo = "Recensione "+rec_id
    #context = {'recensione':recensione, 'titolo':titolo}
    #return render(request, url_detail, context)

# View dettaglio semplificata by DetailView
class DetailView (generic.DetailView):
	model = Recensione
	
	def get_context_data(self, **kwargs):
		context = super(DetailView, self).get_context_data(**kwargs)
		titolo = "Recensione " + str(self.object.pk)
		context['titolo'] = titolo
		return context

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
			# Passo soltanto primi film della lista suggerimenti..
			# Possibili update: passare i primi X % film suggeriti
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
Questa pagina presenta le recensioni più apprezzate, sfruttando numero dei
voti ricevuto e coefficente rank.
La recensione sarà tanto più popolare quanto più è discussa (num_voti) e 
popolare (getRank - coefficente da 0 a 1)!
"""
@method_decorator(login_required(), name='dispatch')
class top100view (generic.ListView):
	template_name = url_index
	
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
Richiede di essere loggati e avere permesso di postare.
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
		if form.is_valid():
			anonRequested = form.cleaned_data['anonymous']
			# Default autore anonimo, aggiorno se non richiesto quindi
			if not anonRequested :
				recensione.autore = request.user
				if isOfficial(request.user):
					recensione.rank = 80
			recensione.save()
			form.save_m2m()
			messages.add_message(request, messages.INFO, 
						'Ottimo, la tua recensione è stata inserita!')
			return HttpResponseRedirect(reverse('recensioni:elenco', kwargs={'filterStr':''}))
		else:
			messages.add_message(request, messages.INFO, 
						'Errore: Hai inserito un tipo di dato non valido.')
			return HttpResponseRedirect(reverse('recensioni:nuovarec'))

# Stesso funzionamento dell'inserimento di nuove recensioni
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
		recensione.__rankUpdate__() 
		return render(request, url_detail, {'recensione':recensione})
