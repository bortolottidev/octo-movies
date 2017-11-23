from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from portal.forms import ContactForm, SignupForm
from portal.models import UserProfile
from portal.utility import anonymous

from LD_Proj.settings import URL_FORM, HOME_URL

HOME_REG_URL = 'portal/index.html'

# View della pagina home degli utenti registrati
@login_required
def welcome(request):
	context = {'request':request,'titolo':'Welcome!', 'homepage':'portal'}
	return render(request, HOME_REG_URL, context)

"""
View della pagina dei contatti
Elabora il form necessario a contattare un admin.
Attualmente non è stato configurato del tutto, bisogna fare modifiche
a settings per poter effettivamente inviare mail.
"""
def contatti(request):
	if request.method == 'POST': #invio
		form = ContactForm(request.POST)
		if form.is_valid():
			soggetto = form.cleaned_data['soggetto']
			messaggio = form.cleaned_data['messaggio']
			email = form.cleaned_data['email']
			invia_copia = form.cleaned_data['invia_copia']
			recipients = ['88744@studenti.unimore.it']
			if invia_copia:
				recipients.append(email)
			#	#	#	#	#	#	#	#
			# SEND MAIL DA CONFIGURARE	#
			#	#	#	#	#	#	#	#
			messages.add_message(request, messages.INFO, 
						'Grazie, la tua mail è stata inoltrata.')
			return HttpResponseRedirect(HOME_URL)
		else:
			messages.add_message(request, messages.INFO, 
						'Errore: Sicuro di aver immesso la mail giusta?')
			return HttpResponseRedirect(reverse('home_reg:contatti'))
	else: # visualizzazione
		form = ContactForm()
		context = {'form':form, 'titolo':'Contatti'}
		return render(request, URL_FORM, context)

# View della pagina per l'iscrizione
def signup (request):
	if request.method == 'GET' :
		form = SignupForm()
		context = {'form':form, 'titolo':'Iscrizione'}
		return render(request, URL_FORM, context)
	else :
		form = SignupForm(request.POST)
		if form.is_valid():
			if form.cleaned_data['password'] != \
				form.cleaned_data['repeat_password'] :
				# ERRORE - Password diverse
				messages.add_message(request, messages.INFO, 
					'Le due password non sono uguali!')
				return HttpResponseRedirect(reverse('home_reg:iscrizione'))
			new_user = form.save(commit=False)
			# OK
			new_user.set_password(form.cleaned_data['password'])
			new_user.is_active = False
			new_user.save()
			messages.add_message(request, messages.INFO, 
						'Ti sei iscritto correttamente! Attendi la convalida di un admin.')
			return HttpResponseRedirect(HOME_URL)
		else:
			if 'username' not in form.cleaned_data:
				messages.add_message(request, messages.INFO, 
					'Spiacente, questo username è già stato preso..')
			else:
				# ERRORE - Generico
				messages.add_message(request, messages.INFO, 
					'Qualcosa è andato storto, riprova..')
			return HttpResponseRedirect(reverse('home_reg:iscrizione'))
