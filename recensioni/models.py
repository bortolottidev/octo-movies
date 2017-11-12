from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_list_or_404
from django.conf import settings

from portal.utility import anonymous
from LD_Proj.utility import objectExist

# I primi voti rendono il rank troppo casuale, quindi preferisco mantenere il
# valore iniziale "neutro" fino a n. 
MIN_VOTE_REQUIRED = 2

""" 
Modello per la recensione.
Partiamo dalla supposizione che, data la presenza dell'AutoField, di un film
possano esservi più recensioni. Una recensione corrisponderà ad un film tramite
il titolo (che non sarà quindi un titolo "per attrarre" ma per classificare).
Uso l'associazione 1:n per l'autore, per poter risalire a tutte le sue
recensioni e l'associazione molti-a-molti per i tag, in quanto ad un tag
corrispondono m film, e ad un film corrispono m tag.
"""
class Recensione(models.Model):
	titolo = models.CharField(max_length=50)
	autore = models.ForeignKey(settings.AUTH_USER_MODEL, 
							on_delete=models.CASCADE, default=anonymous())
	testo = models.TextField()
	voto = models.IntegerField()
	genere = models.CharField(max_length=50, default='sconosciuto')
	pub_date = models.DateTimeField('date_published', auto_now_add=True)
	rank = models.IntegerField(default=50)
	nclicks = models.IntegerField(default=0)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if self.voto is None :
			self.voto = 0
		elif (self.voto > 10) :
			self.voto = 10
		elif (self.voto < 1) :
			self.voto = 1
		if (self.genere == '') :
			self.genere = 'sconosciuto'
		self.__rankUpdate__()
		
	def __str__(self):
		return self.titolo
	
	def getRank (self):
		return self.rank
	
	"""
	forzo aggiornamento del rank dopo ogni recensioni ma aggiorno 
	controllando tutte: possibile miglioramento evitando questo calcolo.
	"""
	def __rankUpdate__(self):
		if objectExist(self, "commento_set"):
			voti_tot = self.commento_set.count()
		else:
			return
		if (voti_tot <= MIN_VOTE_REQUIRED): 
			return 
		voti_pos = 0
		voti_neg = 0
		for commento in self.commento_set.all():
			if commento.voto == True:	# Commento positivo
				voti_pos = voti_pos+1
			elif commento.voto == False: # Commento negativi
				voti_neg = voti_neg+1
		# i voti sono pesati, un voto positivo influisce maggiormente rispetto
		# ad un voto nullo o negativo
		voti_null = (voti_tot - voti_neg - voti_pos)*0.5
		voti_neg = voti_neg*0.5
		# tolgo il "peso" di troppo - complementare a quanto sto usando
		voti_tot = voti_tot - (voti_null*0.5) - (voti_neg*0.5)
		ratio = (voti_null + voti_pos - voti_neg) / voti_tot
		try:
			if (ratio < 0) or (ratio > 1):
				raise Exception(1234, "Ratio isn't a ratio!")
			pass
		except:
			self.rank = 50
			return ; 
		else:
			self.rank = ratio*100
			return ;
	
	# Aumenta il counter del numero di visite alla recensione
	def counterClicksUp(self):
		self.nclicks = self.nclicks + 1
		self.save()

	# Campi che vogliamo far visualizzare nell'interfaccia admin
	def campi():
		return ['titolo', 'testo', 'voto', 'genere',
		  'autore', 'rank', 'nclicks' ]
	
	# Campi non modificabili
	def __campiSegreti__():
		return ['rank', 'autore', ]
	
	def num_voti(self):
		return self.commento_set.count() 
		
	def breve(self):
		testo_breve = self.testo[0:250]
		prime_righe = testo_breve.split('.')
		if len(prime_righe) != 1:
			sep = '.'
			return sep.join(prime_righe[:-1])+"."
		return testo_breve[:248]+".."
		
	def getAutore(self):
		return self.autore
	
	# NB Ritorna una lista, non un queryset!
	def __allRec__():
		lista = get_list_or_404(Recensione.objects.order_by('-pub_date'))
		return lista
	
# Il voto alla recensione avviene attraverso il NullBooleanField, che prevede
# anche un eventuale voto Null ovvero neutrale.
class Commento(models.Model):
	# Default .id per evitare problemi di serializzazione
	recensione = models.ForeignKey(Recensione, on_delete=models.CASCADE,
								default=Recensione.__allRec__()[0].id)
	autore = models.ForeignKey(settings.AUTH_USER_MODEL, 
							on_delete=models.CASCADE, default=anonymous())
	voto = models.NullBooleanField(default=0)
	testo = models.TextField(max_length=150, blank=True)
		
	# Campi visualizzabili in interfaccia admin
	def __campi__():
		return ['recensione', 'autore', 'voto', 'testo']
	# Campi non modificabili 
	def __campisegreti__():
		return ['recensione', ]	
	def __str__(self):
		return self.testo
    
"""    
 Modello per i tag associati ad una recensione di un film
 Vogliamo che ogni tag sia unico, quindi la primary key sarà il tag stesso
 e non il "classico" AutoField.
"""
class Tag(models.Model):
    nome = models.CharField(max_length=25, primary_key=True)
    recensione = models.ManyToManyField(Recensione)
    
    def __str__(self):
        return self.nome
