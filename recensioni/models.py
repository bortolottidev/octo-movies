from django.db import models
from django.contrib.auth.models import User
from LD_Proj import settings
from django.conf import settings
from portal.utility import anonymous
from LD_Proj.utility import objectExist

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
	
	# Migliora aggiornando solo l'ultimo voto
	def __rankUpdate__(self):
		if objectExist(self, "commento_set"):
			voti_tot = self.commento_set.count()
		else:
			return
		# I primi voti rendono il rank troppo casuale. In una situazione vera
		# prenderei un numero più elevato.
		if (voti_tot <= 2): 
			return 
		voti_pos = 0
		voti_neg = 0
		for commento in self.commento_set.all():
			if commento.voto == True:	# Commento positivo
				voti_pos = voti_pos+1
			elif commento.voto == False: # Commento negativi
				voti_neg = voti_neg+1
		# i voti sono pesati, non voglio influiscano ugualmente
		voti_null = (voti_tot - voti_neg - voti_pos)*0.5
		voti_neg = voti_neg*0.5
		# tolgo il "peso" di troppo - complementare a quanto sto usando
		voti_tot = voti_tot - (voti_null*0.5) - (voti_neg*0.5)
		ratio = (voti_null + voti_pos - voti_neg) / voti_tot
		#print("voti null = "+str(voti_null))
		#print("voti pos = "+str(voti_pos))
		#print("voti neg = "+str(voti_neg))
		#print("ratio = "+str(ratio))
		try:
			if (ratio < 0) or (ratio > 1):
				#print("RATIO ERROR ON "+self+": "+str(ratio))
				raise Exception(1234, "Ratio isn't a ratio!")
			pass
		except:
			self.rank = 50
			return ; 
		else:
			self.rank = ratio*100
			return ;
	
	def campi():
		return ['titolo', 'testo', 'voto', 'genere',
		  'autore', 'rank', ]
	
	def campi_segreti():
		return ['rank', ]
	
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
	
	def __allRec__():
		if not Recensione.objects.all() :
			return [None]
		return Recensione.objects.all()
	
# Modello per i commenti alla recensione (1:n rispetto ad essa)
# Il voto alla recensione avviene attraverso il NullBooleanField che prevede
# anche un eventuale voto Null ovvero neutrale.
class Commento(models.Model):
	recensione = models.ForeignKey(Recensione, on_delete=models.CASCADE,
								default=Recensione.__allRec__()[0])
	autore = models.ForeignKey(settings.AUTH_USER_MODEL, 
							on_delete=models.CASCADE, default=anonymous())
	voto = models.NullBooleanField(default=0)
	testo = models.TextField(max_length=150, blank=True)
		
	def __campi__():
		return ['recensione', 'autore', 'voto', 'testo']
	def __campisegreti__():
		return ['recensione', ]
	
	def __str__(self):
		return self.testo
    
"""    
 Modello per i tag associati ad una recensione di un film
 Vogliamo che ogni tag sia unico, quindi la primary key sarà il tag stesso
 e non il solito AutoField.
"""
class Tag(models.Model):
    nome = models.CharField(max_length=25, primary_key=True)
    recensione = models.ManyToManyField(Recensione)
    
    def __str__(self):
        return self.nome
