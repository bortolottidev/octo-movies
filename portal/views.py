from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from portal.forms import ContactForm
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
